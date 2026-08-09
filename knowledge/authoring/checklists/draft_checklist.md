# Draft Checklist

**Use before:** `draft` → `internal_review`  
**Package:** `{{PACKAGE_ID}}` `{{PACKAGE_VERSION}}`  
**Author:** `{{AUTHOR}}` — Date: `{{DATE}}`

---

## Identity

- [ ] Folder name equals `package_id`
- [ ] `package_id` matches naming rules and is not reused
- [ ] `package_type` and `domain_id` set; domain exists in taxonomy
- [ ] `schema_version` is `2.0.0`; `package_spec_version` is `1.0.0`
- [ ] `status` is `draft`
- [ ] Version is SemVer; version not encoded in ids
- [ ] Primary `language` is BCP 47

## Files

- [ ] `PACKAGE.json` present (from template)
- [ ] `MANIFEST.json` present and consistent with identity
- [ ] `README.md` describes purpose and out of scope
- [ ] `CHANGELOG.md` has an Unreleased or `0.1.0` section
- [ ] Component paths in the manifest exist

## Content

- [ ] No production analytical rules invented for “placeholder” meaning
- [ ] Unknown classical claims marked `TODO_REVIEW`
- [ ] Exported ids reserved and unique in the working set
- [ ] Dependencies declared or explicitly empty
- [ ] Examples are pedagogical, not Golden Dataset expected output

## Self-validation

- [ ] Intended validation profile recorded (`PVP-MINIMAL` minimum)
- [ ] [CHECKLIST.md](../CHECKLIST.md) completed for any KR records inside the package

Author sign-off: `{{AUTHOR}}`
