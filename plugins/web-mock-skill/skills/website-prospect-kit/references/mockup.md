# Building a credible concept

## Derive a direction from this brand

Use the prospect's actual logo, palette, content voice, image treatment, and offer. Record an internal design brief before building: audience, primary visitor task, conversion goal, retained brand elements, and the two or three assessment findings the composition should address.

For ecommerce, product discovery, meaningful differences, fit guidance, and purchasing paths usually matter. For a local service, service area, offer clarity, credibility, hours, and contact/booking may matter more. For B2B, clarify the audience, use cases, supporting evidence, and inquiry path. Do not force every site into a four-product grid or invent a catalog to fill space.

Use a deliberate type hierarchy, content width, spacing system, and image composition. A strong hero should state a relevant benefit and lead to an appropriate next action. The rest of the page should add useful information instead of repeating the hero. Choose sections by the specific visitor journey, not a requirement to fill a long page.

## Asset handling

Inspect images at useful resolution. Original source often has low-resolution `src` placeholders and real images in `srcset`, `data-srcset`, `data-src`, inline styles, or structured product data. Resolve relative URLs against the page. Keep filenames and source mappings traceable; inspect redirects and successful downloads before using assets.

Avoid enlarging a 20-pixel placeholder. Do not crop important product features, people, or baked-in copy. When a supplied banner contains text, prefer the original underlying photograph if available; otherwise choose another suitable image or carefully crop a purely photographic region and verify every target aspect ratio. Preserve original transparency. Build simple decorative waves and interface icons with CSS or inline SVG, not fabricated product photos or imitation logos.

Download assets without copying third-party analytics, advertising code, embedded forms, or the prospect's entire source into the demo. No API keys are needed for this workflow. If provided source includes tokens or personal information, exclude them from generated output and any repository publication.

## Interaction choices

Only add controls that support the proposal. A local product filter can operate on a small, honest sample of the catalog; label that scope. Search must make its scope clear and show a useful no-results state. Product details should lead to the real store for size/variant choice instead of implying the demo has live inventory.

Use links for destinations and buttons for actions. Mobile menus expose their expanded state, overlays have a named close control and appropriate dialog behavior, visible controls work with the keyboard, and form fields have labels. Do not display an email subscription or contact form that silently discards submissions. A contact link is often sufficient for a dummy site.

Use one H1, meaningful section headings, sensible image alternatives, explicit image sizing where possible, and a useful page title/description. Do not advertise an accessibility compliance level without a proper audit. Treat structured data in an unpublished demo as illustrative; never insert fake ratings or entities.

## Verification and packaging

Inspect at a desktop size and a narrow phone size, and spot-check an intermediate width when practical. Use actual device emulation or check the layout viewport before treating a screenshot as mobile evidence. Check any filters, modal dialogs, menus, and search paths the page contains. Inspect below the fold too. Make the page useful without motion; avoid horizontal overflow and illegible labels.

Record which checks ran and which did not. Broken image requests, dead primary links, clipped important text, and inert CTAs are fixes to complete before handoff. Avoid unnecessary test frameworks for a static prototype; simple targeted checks are enough.

The default package is local HTML and assets. Publishing requires user instruction and appropriate tools/access. If a hosting skill is installed and relevant, follow it within the user's requested scope; retain a requested local-only output. A localhost URL is not a shareable client preview.
