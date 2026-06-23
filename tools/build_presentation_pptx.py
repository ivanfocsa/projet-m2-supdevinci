from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Presentation_Daylight_CyberTrust.pptx"

SLIDES = [
    ("Daylight / Cyber Trust", "Mise en place d'un SOC externalise\nProjet 4 - Mastere Cybersecurite", ["Kilyan FELIX", "Yvan FOCSA", "Youssef GUERNIOU", "Mahamadou DIACOUMBA"]),
    ("Contexte Daylight", "Reseau d'audioprothesistes multi-site", ["Environ trente centres en France", "Donnees sensibles : CRM, RDV, dossiers patients", "Besoin de visibilite cyber et de reaction", "Manque de ressources SOC internes"]),
    ("Objectifs du SOC", "Ce que Cyber Trust doit livrer", ["Collecte multi-source", "SIEM open-source centralise", "Alertes personnalisables", "Dashboards lisibles", "Playbooks et REX", "Guide de deploiement et video"]),
    ("Equipe Cyber Trust", "Repartition des roles", ["Yvan FOCSA : architecte de la solution", "Youssef GUERNIOU : SIEM / Wazuh", "Kilyan FELIX : chef de projet SOC, detection", "Mahamadou DIACOUMBA : exploitation, VM, playbooks, REX"]),
    ("Architecture demo", "Lab reproductible Wazuh", ["Wazuh Manager, Indexer et Dashboard", "poste-01 : endpoint Windows", "serveur-01 : serveur Linux simule", "Logs Daylight : CRM, RDV, dossiers patients", "Interface web Wazuh Dashboard"]),
    ("Architecture cible", "Industrialisation pour les centres Daylight", ["Separation Manager / Indexer / Dashboard", "Collecte agents, syslog et API", "Dashboards par role et par site", "Retention et stockage dimensionnes", "Deploiement progressif multi-centres"]),
    ("Demonstration SIEM", "Travail de Youssef", ["Wazuh 4.14.5 en Docker single-node", "Script setup-siem-lab.ps1", "Creation de serveur-01", "Agent Wazuh, SSH, rsyslog", "Simulation brute force SSH"]),
    ("Sources de logs", "Couverture du cahier des charges", ["Endpoint : poste-01", "Serveur : serveur-01", "Application metier : Daylight", "Evenements systeme, endpoint et metier", "Base extensible vers firewall, AD, messagerie"]),
    ("Alertes cles", "Scenarios a montrer", ["5712 : brute force SSH", "100110 : brute force applicatif", "100120 : acces anormal dossier patient", "100130 : modification groupe privilegie", "100140 : usage USB suspect"]),
    ("Dashboards", "Lecture analyste et supervision", ["Dashboard technique : severite, source, top regles", "Dashboard executif : volume, critiques, sites", "Vision lisible pour le client", "Support de qualification et reporting"]),
    ("Qualification SOC", "Priorisation des alertes", ["Critique : donnees patient, privileges", "Haute : brute force confirme", "Moyenne : USB ou anomalie contextuelle", "Basse : hygiene et conformite", "Objectif : reduire le bruit"]),
    ("RBAC", "Segmentation par roles", ["Admin : configuration complete", "Analyste : lecture alertes et dashboards", "Supervision : reporting", "Role soc_readonly", "Repond a l'exigence supervision / analyste / admin"]),
    ("Playbooks", "Reponse operationnelle", ["Triage initial", "Brute force SSH", "Acces anormal dossier patient", "Brute force applicatif", "Modification privilege", "USB suspect et phishing"]),
    ("REX incidents", "Amelioration continue", ["Brute force SSH : verifier succes apres echecs", "Acces patient : verifier profil et justification", "Privilege : controler demande de changement", "Documenter preuves, decisions, actions"]),
    ("Exploitation du lab", "Procedure de redemarrage", ["Demarrer Wazuh depuis sa racine technique", "docker start serveur-01", "Relancer rsyslogd et SSH", "Relancer l'agent Wazuh", "Finaliser avec post_capture_finalize.ps1"]),
    ("Couts et industrialisation", "Passer du lab a la production", ["Wazuh limite les couts de licence", "Couts principaux : infrastructure, stockage, exploitation", "Pilote sur quelques centres", "Generalisation progressive", "Reporting et SLA Cyber Trust"]),
    ("Limites", "Points a renforcer", ["Single-node non HA", "Firewall, messagerie et AD a completer", "Retention et volumetrie a dimensionner", "Ticketing / SOAR a connecter", "Captures finales a ajouter"]),
    ("Conclusion", "Une base SOC claire et evolutive", ["Collecte multi-source", "Detections et dashboards", "RBAC", "Playbooks et REX", "Documentation et guide", "Solution industrialisable pour Daylight"]),
]


def xml(text: str) -> str:
    return escape(text, {"'": "&apos;", '"': "&quot;"})


def text_box(idx: int, x: int, y: int, w: int, h: int, text: str, size: int = 2400, bold: bool = False, color: str = "111827") -> str:
    runs = []
    for line in text.split("\n"):
        runs.append(
            f"""
            <a:p>
              <a:r>
                <a:rPr lang="fr-FR" sz="{size}" b="{1 if bold else 0}">
                  <a:solidFill><a:srgbClr val="{color}"/></a:solidFill>
                </a:rPr>
                <a:t>{xml(line)}</a:t>
              </a:r>
            </a:p>"""
        )
    return f"""
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="{idx}" name="TextBox {idx}"/>
          <p:cNvSpPr txBox="1"/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="{x}" y="{y}"/>
            <a:ext cx="{w}" cy="{h}"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln><a:noFill/></a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square"/>
          <a:lstStyle/>
          {''.join(runs)}
        </p:txBody>
      </p:sp>"""


def bullet_box(idx: int, bullets: list[str]) -> str:
    paragraphs = []
    for bullet in bullets:
        paragraphs.append(
            f"""
            <a:p>
              <a:pPr marL="342900" indent="-171450">
                <a:buChar char="â€¢"/>
              </a:pPr>
              <a:r>
                <a:rPr lang="fr-FR" sz="2350">
                  <a:solidFill><a:srgbClr val="1f2937"/></a:solidFill>
                </a:rPr>
                <a:t>{xml(bullet)}</a:t>
              </a:r>
            </a:p>"""
        )
    return f"""
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="{idx}" name="Bullets {idx}"/>
          <p:cNvSpPr txBox="1"/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="820000" y="2100000"/>
            <a:ext cx="10300000" cy="4300000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln><a:noFill/></a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr wrap="square"/>
          <a:lstStyle/>
          {''.join(paragraphs)}
        </p:txBody>
      </p:sp>"""


def slide_xml(title: str, subtitle: str, bullets: list[str], n: int) -> str:
    accent = "0f766e" if n % 3 == 1 else "1d4ed8" if n % 3 == 2 else "7c2d12"
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg>
      <p:bgPr>
        <a:solidFill><a:srgbClr val="f8fafc"/></a:solidFill>
        <a:effectLst/>
      </p:bgPr>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Accent"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="220000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="{accent}"/></a:solidFill>
          <a:ln><a:noFill/></a:ln>
        </p:spPr>
      </p:sp>
      {text_box(3, 690000, 520000, 10800000, 720000, title, 3900, True, "0f172a")}
      {text_box(4, 720000, 1320000, 10500000, 530000, subtitle, 2150, False, accent)}
      {bullet_box(5, bullets)}
      {text_box(6, 9700000, 6500000, 1800000, 260000, f"Slide {n}", 1250, False, "64748b")}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def rels_xml(targets: list[tuple[str, str, str]]) -> str:
    rels = []
    for idx, (rtype, target, rid) in enumerate(targets, 1):
        rid_value = rid or f"rId{idx}"
        rels.append(f'<Relationship Id="{rid_value}" Type="{rtype}" Target="{target}"/>')
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{''.join(rels)}
</Relationships>"""


def content_types(slide_count: int) -> str:
    overrides = [
        ('/ppt/presentation.xml', 'application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml'),
        ('/ppt/slideMasters/slideMaster1.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml'),
        ('/ppt/slideLayouts/slideLayout1.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'),
        ('/ppt/theme/theme1.xml', 'application/vnd.openxmlformats-officedocument.theme+xml'),
    ]
    for i in range(1, slide_count + 1):
        overrides.append((f'/ppt/slides/slide{i}.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml'))
    ov = "\n".join(f'<Override PartName="{part}" ContentType="{ctype}"/>' for part, ctype in overrides)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  {ov}
</Types>"""


PRESENTATION_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>
    {slide_ids}
  </p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
  <p:defaultTextStyle/>
</p:presentation>"""

SLIDE_MASTER = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>"""

SLIDE_LAYOUT = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""

THEME = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Cyber Trust">
  <a:themeElements>
    <a:clrScheme name="Cyber Trust">
      <a:dk1><a:srgbClr val="111827"/></a:dk1><a:lt1><a:srgbClr val="ffffff"/></a:lt1>
      <a:dk2><a:srgbClr val="1f2937"/></a:dk2><a:lt2><a:srgbClr val="f8fafc"/></a:lt2>
      <a:accent1><a:srgbClr val="0f766e"/></a:accent1><a:accent2><a:srgbClr val="1d4ed8"/></a:accent2>
      <a:accent3><a:srgbClr val="7c2d12"/></a:accent3><a:accent4><a:srgbClr val="334155"/></a:accent4>
      <a:accent5><a:srgbClr val="be123c"/></a:accent5><a:accent6><a:srgbClr val="4b5563"/></a:accent6>
      <a:hlink><a:srgbClr val="2563eb"/></a:hlink><a:folHlink><a:srgbClr val="7c3aed"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Segoe"><a:majorFont><a:latin typeface="Segoe UI"/></a:majorFont><a:minorFont><a:latin typeface="Segoe UI"/></a:minorFont></a:fontScheme>
    <a:fmtScheme name="Default"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme>
  </a:themeElements>
</a:theme>"""


def build() -> None:
    slide_ids = "\n".join(f'<p:sldId id="{256 + i}" r:id="rId{i + 1}"/>' for i in range(1, len(SLIDES) + 1))
    presentation_rels = [
        ("http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "slideMasters/slideMaster1.xml", "rId1")
    ]
    for i in range(1, len(SLIDES) + 1):
        presentation_rels.append(("http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide", f"slides/slide{i}.xml", f"rId{i + 1}"))

    with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types(len(SLIDES)))
        z.writestr("_rels/.rels", rels_xml([("http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument", "ppt/presentation.xml", "rId1")]))
        z.writestr("ppt/presentation.xml", PRESENTATION_XML.format(slide_ids=slide_ids))
        z.writestr("ppt/_rels/presentation.xml.rels", rels_xml(presentation_rels))
        z.writestr("ppt/slideMasters/slideMaster1.xml", SLIDE_MASTER)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", rels_xml([
            ("http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml", "rId1"),
            ("http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "../theme/theme1.xml", "rId2"),
        ]))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", SLIDE_LAYOUT)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", rels_xml([
            ("http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "../slideMasters/slideMaster1.xml", "rId1")
        ]))
        z.writestr("ppt/theme/theme1.xml", THEME)
        for i, (title, subtitle, bullets) in enumerate(SLIDES, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xml(title, subtitle, bullets, i))
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", rels_xml([
                ("http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml", "rId1")
            ]))

    print(f"PPTX genere : {OUT}")


if __name__ == "__main__":
    build()



