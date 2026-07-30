#!/usr/bin/env node
/**
 * Validate Knowledge Schema Foundation with AJV (Draft 2020-12).
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = __dirname;

const ajv = new Ajv2020({
  allErrors: true,
  strict: false,
  validateSchema: true,
});
addFormats(ajv);

const files = fs
  .readdirSync(root)
  .filter((name) => name.endsWith(".schema.json"))
  .sort();

const schemas = files.map((name) => {
  const full = path.join(root, name);
  const schema = JSON.parse(fs.readFileSync(full, "utf8"));
  return { name, schema };
});

for (const { name, schema } of schemas) {
  ajv.addSchema(schema, schema.$id);
  ajv.addSchema(schema, name);
}

const errors = [];
for (const { name, schema } of schemas) {
  try {
    const validate = ajv.compile(schema);
    // compile success proves refs resolve for AJV
    if (typeof validate !== "function") {
      errors.push(`${name}: compile did not return validator`);
    }
  } catch (err) {
    errors.push(`${name}: ${err.message}`);
  }
}

// Sample instance for five_element
const sample = {
  identity: {
    knowledge_id: "KNO-000001",
    canonical_name: "Wood",
    chinese: "木",
    pinyin: "mu",
    english_name: "Wood",
  },
  classification: { domain: "five_elements", category: "element" },
  definition: "Structural placeholder definition for schema validation only.",
  characteristics: { nature: "growth" },
  relationships: {},
  references: [{ reference_id: "REF-000001", title: "Placeholder Source" }],
  metadata: { version: "1.0.0", status: "draft", schema_version: "1.0.0" },
  validation: {
    schema_valid: true,
    reference_valid: true,
    relationship_valid: true,
    integrity_valid: true,
  },
  revision_history: [
    { version: "1.0.0", date: "2026-07-30", summary: "schema foundation sample" },
  ],
  correspondences: { season: "spring", direction: "east" },
};

const fiveValidate = ajv.getSchema(
  "https://bte-platform.org/schema/knowledge/five_element.schema.json"
);
if (!fiveValidate) {
  errors.push("five_element schema not registered in AJV");
} else if (!fiveValidate(sample)) {
  for (const err of fiveValidate.errors || []) {
    errors.push(`five_element sample: ${err.instancePath} ${err.message}`);
  }
}

if (errors.length) {
  console.log("AJV VALIDATION FAILED");
  for (const item of errors) console.log(` - ${item}`);
  process.exit(1);
}

console.log("AJV VALIDATION PASSED");
console.log(`schemas_checked=${files.length}`);
console.log("draft=2020-12");
console.log("engine=ajv");
