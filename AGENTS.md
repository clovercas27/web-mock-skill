# Working in this repository

This repository contains the Website Prospect Kit skill and its plugin packaging.

When the user supplies a prospect URL with screenshots and/or source and asks for a kit, assessment, mockup, or outreach, read `plugins/web-mock-skill/skills/website-prospect-kit/SKILL.md` and follow its applicable scope. For the complete kit, produce all three deliverables without asking the user to repeat the workflow.

Keep generated prospect work outside tracked package files, preferably in the ignored `prospects/` directory. Do not commit prospect source, screenshots, copied logos/product images, contact lists, credentials, or browser profiles unless the user explicitly requests publication of those materials. A kit request authorizes local artifact generation, not sending outreach or modifying a prospect's website.

For edits to the skill, retain the boundary between sourced findings and untested hypotheses, local HTML output by default, and draft-only outreach. Run the source-helper tests after helper changes. Validate skill frontmatter and all JSON manifests before uploading package changes. Do not claim this repository has been installed in ChatGPT solely because it was pushed to GitHub.
