import base64, uuid, requests
from datetime import datetime, timezone, timedelta
import lxml.etree as etree
import xmlsec
from cachetools import TTLCache

SAML_NS = "urn:oasis:names:tc:SAML:2.0:assertion"
_token_cache = TTLCache(maxsize=4096, ttl=23 * 60 * 60)

def _ts(delta_minutes=0):
    t = datetime.now(timezone.utc) + timedelta(minutes=delta_minutes)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")

def _build_assertion(user_id, token_url, api_key, issuer):
    instant = _ts()
    a = etree.Element(
        f"{{{SAML_NS}}}Assertion",
        attrib={"ID": f"_{uuid.uuid4()}", "Version": "2.0", "IssueInstant": instant},
        nsmap={"saml2": SAML_NS, "xs": "http://www.w3.org/2001/XMLSchema",
               "xsi": "http://www.w3.org/2001/XMLSchema-instance"},
    )
    etree.SubElement(a, f"{{{SAML_NS}}}Issuer").text = issuer
    subj = etree.SubElement(a, f"{{{SAML_NS}}}Subject")
    nid = etree.SubElement(subj, f"{{{SAML_NS}}}NameID",
                           Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified")
    nid.text = user_id
    sc = etree.SubElement(subj, f"{{{SAML_NS}}}SubjectConfirmation",
                          Method="urn:oasis:names:tc:SAML:2.0:cm:bearer")
    etree.SubElement(sc, f"{{{SAML_NS}}}SubjectConfirmationData",
                     NotOnOrAfter=_ts(5), Recipient=token_url)
    cond = etree.SubElement(a, f"{{{SAML_NS}}}Conditions",
                            NotBefore=_ts(-5), NotOnOrAfter=_ts(5))
    ar = etree.SubElement(cond, f"{{{SAML_NS}}}AudienceRestriction")
    etree.SubElement(ar, f"{{{SAML_NS}}}Audience").text = "www.successfactors.com"
    authn = etree.SubElement(a, f"{{{SAML_NS}}}AuthnStatement",
                             AuthnInstant=instant, SessionIndex=str(uuid.uuid4()))
    actx = etree.SubElement(authn, f"{{{SAML_NS}}}AuthnContext")
    etree.SubElement(actx, f"{{{SAML_NS}}}AuthnContextClassRef").text = (
        "urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport")
    attrs = etree.SubElement(a, f"{{{SAML_NS}}}AttributeStatement")
    attr = etree.SubElement(attrs, f"{{{SAML_NS}}}Attribute", Name="api_key")
    etree.SubElement(attr, f"{{{SAML_NS}}}AttributeValue").text = api_key
    return a

def _sign(assertion, private_key_pem):
    key = xmlsec.Key.from_memory(private_key_pem, xmlsec.constants.KeyDataFormatPem)
    xmlsec.tree.add_ids(assertion, ["ID"])
    sig = xmlsec.template.create(assertion, xmlsec.constants.TransformExclC14N,
                                 xmlsec.constants.TransformRsaSha256, ns="ds")
    assertion.insert(0, sig)
    ref = xmlsec.template.add_reference(sig, xmlsec.constants.TransformSha256,
                                        uri="#" + assertion.attrib["ID"])
    xmlsec.template.add_transform(ref, xmlsec.constants.TransformEnveloped)
    xmlsec.template.add_transform(ref, xmlsec.constants.TransformExclC14N)
    xmlsec.template.ensure_key_info(sig)
    ctx = xmlsec.SignatureContext()
    ctx.key = key
    ctx.sign(xmlsec.tree.find_node(assertion, xmlsec.constants.NodeSignature))
    return assertion

def _encode(assertion):
    xml = b'<?xml version="1.0" encoding="UTF-8"?>' + etree.tostring(assertion)
    return base64.b64encode(xml).decode()

def get_user_token(sf_user_id, host, company_id, client_id, private_key_pem, issuer):
    cached = _token_cache.get(sf_user_id)
    if cached:
        return cached
    token_url = f"{host}/oauth/token"
    assertion = _encode(_sign(_build_assertion(sf_user_id, token_url, client_id, issuer),
                              private_key_pem))
    resp = requests.post(
        token_url,
        data={"company_id": company_id, "client_id": client_id,
              "grant_type": "urn:ietf:params:oauth:grant-type:saml2-bearer",
              "assertion": assertion},
        headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=20)
    resp.raise_for_status()
    token = resp.json()["access_token"]
    _token_cache[sf_user_id] = token
    return token

