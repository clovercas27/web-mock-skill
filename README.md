# Website Prospect Kit

Supply a website URL, screenshots, and page source. Get a website assessment, branded HTML redesign concept, and outreach email you can send.

This repository packages the workflow as a reusable agent skill inside a skills-only plugin. It has no MCP server, hosting service, API key, paid API call, email sender, or background trigger. Your ChatGPT/Codex environment supplies the model and any browsing, code, file, and preview tools. Connecting GitHub makes repository content accessible; it does not, by itself, install or run this workflow.

## Use it in ChatGPT

Choose the supported installation path for your account:

- **ChatGPT desktop:** add this GitHub repository as a plugin marketplace using `codex plugin marketplace add clovercas27/web-mock-skill` from an installed Codex CLI, then open the desktop Plugins Directory and install Website Prospect Kit from that source. Restart or refresh as required by the client.
- **Workspace with plugin import:** a workspace admin can use **Admin > Plugins > Add > Import marketplace** with this repository and its `.agents/plugins/marketplace.json` catalog. Install/enable the imported plugin for the intended users. Availability depends on workspace controls.
- **Custom GPT fallback:** use [CHATGPT-INSTRUCTIONS.md](CHATGPT-INSTRUCTIONS.md) and its listed knowledge files. This is a separate manual setup, useful when plugin import is unavailable.

After installation, select the skill/plugin in ChatGPT and supply:

```text
Create the complete prospect kit for https://the-prospect-site.example/

Attached: brand screenshots and current page source.
```

The example domain is a placeholder; replace it with the actual prospect's URL. In Codex, explicitly invoke `$website-prospect-kit` after installing the standalone skill. In ChatGPT, use the available `@` selector. Automatic selection can also apply when the installed skill matches your request. This means one requested run completes the deliverables; it is not an automatic background action whenever a file is uploaded.

Official setup references: [Skills and discovery](https://learn.chatgpt.com/docs/build-skills), [Plugin packaging and marketplaces](https://developers.openai.com/plugins/build/plugins), and [GitHub marketplace import](https://learn.chatgpt.com/docs/enterprise/plugin-management). Verified November 11, 2026. Installation on your account must be verified separately from validating the repository files.

## Standalone Codex skill

Ask Skill Installer:

```text
$skill-installer install the skill from https://github.com/clovercas27/web-mock-skill at plugins/web-mock-skill/skills/website-prospect-kit
```

Alternatively, copy that `website-prospect-kit` folder into a supported local skill directory, preserving its references/scripts. Follow your client's current skill-location documentation. Installation is not required merely to read this repository and explicitly ask an agent to follow its skill instructions.

## Outputs per prospect

```text
brand-proposal/
  ASSESSMENT.md          prioritized observations and recommendations
  OUTREACH.md            subject options, first email and follow-up
  SOURCES.md             evidence and brand asset provenance
  VERIFICATION.md        checks actually run and remaining limitations
  mockup/
    index.html
    styles.css
    app.js               when interactions need it
    assets/
  desktop-preview.png    when browser capture is available
  mobile-preview.png     when browser capture is available
brand-proposal.zip       when file tools are available
```

The skill adapts to ecommerce, service businesses, and B2B sites. It defaults to local dummy HTML, retains branding, uses real evidence, and drafts email without sending. It does not promise rankings, AI citations, or conversion lifts. If a capability is unavailable, it reports the limitation and completes the deliverables the environment supports.

## Repository structure

```text
.agents/plugins/marketplace.json
plugins/web-mock-skill/plugin.json
plugins/web-mock-skill/skills/website-prospect-kit/
  SKILL.md
  agents/openai.yaml
  references/assessment-and-outreach.md
  references/mockup.md
  scripts/inspect_source.py
CHATGPT-INSTRUCTIONS.md
tests/test_inspect_source.py
```

Keep prospect source, screenshots, credentials, and generated proposals out of this reusable repository. Put outputs in a separate workspace or ignored `prospects/` / `output/` directory. No license is assigned by this initial package; choose one before redistributing it under specific license terms.

## Local verification

The source helper uses Python's standard library and never makes network calls:

```text
python plugins/web-mock-skill/skills/website-prospect-kit/scripts/inspect_source.py page-source.html --base-url https://example.com/ --out inventory.json
python -m unittest discover -s tests -v
```

Use the official Skill Creator `quick_validate.py` to validate skill frontmatter; that validator requires PyYAML. Passing these checks validates the helper and package structure, not the quality of every future generated proposal or a successful installation in your account.
