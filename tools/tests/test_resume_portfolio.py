"""Validate the six public PDF, editable and ATS resume releases."""
from pathlib import Path
from urllib.parse import urlsplit
import json,re,unittest
ROOT=Path(__file__).resolve().parents[2]
R=ROOT/"resumes"
class ResumeReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=json.loads((R/"ARAZVERA_RESUME_PACK_MANIFEST_20261118.json").read_text(encoding="utf-8"))
    def test_six_role_specific_public_resume_pdfs_and_editable_files_exist(self):
        docs=self.m["files"]
        self.assertEqual(len(docs),6)
        self.assertEqual(len({x["base"] for x in docs}),6)
        for e in docs:
            with self.subTest(name=e["base"]):
                pdf=ROOT/e["pdf"]
                self.assertTrue(pdf.is_file())
                self.assertGreater(pdf.stat().st_size,20_000)
                self.assertEqual(pdf.read_bytes()[:4],b"%PDF")
                self.assertTrue((ROOT/e["markdown"]).is_file())
                self.assertTrue((ROOT/e["ats_text"]).is_file())
                self.assertIn("contact.arazvera@gmail.com",(ROOT/e["ats_text"]).read_text(encoding="utf-8"))
    def test_public_resume_does_not_publish_private_source_or_tokens(self):
        for entry in self.m["files"]:
            txt=(ROOT/entry["markdown"]).read_text(encoding="utf-8")
            self.assertNotIn("arazvera-source-bank-private-44",txt)
            self.assertNotIn("D:\\ARAZVERA_PRODUCTS",txt)
            self.assertNotRegex(txt,r"(?i)github_pat_[a-z0-9_]{20,}|ghp_[a-z0-9]{20,}|-----BEGIN .*PRIVATE KEY")
    def test_verified_numbers_are_labeled(self):
        m=self.m["verification"]
        self.assertEqual(m["fresh_private_L2_unit_tests"],203)
        self.assertEqual(m["fresh_private_L2_archives"],19)
        self.assertEqual(m["public_buyer_lab_tests"],27)
        self.assertEqual(m["private_archive_SHA_ZIP_check"],44)
        self.assertEqual(m["production_approved_count"],0)
        self.assertEqual(m["sale_license_approved_count"],0)
        overview=(R/"ARAZVERA_Buyer_Proof_Resume_20261118.md").read_text(encoding="utf-8")
        self.assertIn("203 / 203",overview)
        self.assertIn("not references to paid customer deployments",overview)
    def test_all_relative_markdown_links_resolve(self):
        for entry in self.m["files"]:
            p=ROOT/entry["markdown"]
            for href in re.findall(r"\]\(([^)\s]+)\)",p.read_text(encoding="utf-8")):
                with self.subTest(doc=p.name,href=href):
                    if urlsplit(href).scheme in ("https","mailto"):continue
                    target=(p.parent/href.split("#",1)[0]).resolve()
                    self.assertTrue(target.is_relative_to(ROOT))
                    self.assertTrue(target.exists(),str(target))
    def test_portfolio_index_has_new_cv_and_no_literal_newline_escapes(self):
        root=(ROOT/"README.md").read_text(encoding="utf-8")
        index=(R/"README.md").read_text(encoding="utf-8")
        self.assertIn("RESUME_SELECTION_GUIDE_20261118.md",root)
        self.assertIn("ARAZVERA_Complete_Resume_Pack_20261118.zip",root)
        self.assertIn("six-version",index)
        self.assertNotIn(r"\n\n**NEW",root)
if __name__=="__main__":unittest.main()
