# CBV Notes and Design Rationale

This document explains the Class-Based Views (CBVs) implemented in the project, mixin usage, and tradeoffs between FBVs and CBVs.

## Implemented CBVs

- `PostDetailView` (in `blog/views.py`)
  - Composition: `FormMixin` + `DetailView`
  - Purpose: display a single `Post` and accept a `CommentForm` POST to create a comment associated with the post.
  - Key hooks used:
    - `get_context_data` to include `comments` and `form`.
    - `post` to bind the form and call `form_valid`/`form_invalid`.
    - `form_valid` to create the `Comment` and then follow the normal success flow.

- `PostCreateView` (in `blog/views.py`)
  - Composition: `LoginRequiredMixin` + `CreateView`
  - Purpose: allow logged-in users to create posts; `form_valid` sets `form.instance.author = request.user`.

- `PostUpdateView` (in `blog/views.py`)
  - Composition: `LoginRequiredMixin` + `UserPassesTestMixin` + `UpdateView`
  - Purpose: allow post owners to update a post. `test_func` ensures only the author can edit.

- `PostDeleteView` (in `blog/views.py`)
  - Composition: `LoginRequiredMixin` + `UserPassesTestMixin` + `DeleteView`
  - Purpose: allow post owners to delete a post with a confirmation page.

## Why mixins and ordering matter

- Mixins like `LoginRequiredMixin` and `UserPassesTestMixin` are placed left-most (before the generic view) per Django recommendations so that their `dispatch` and `test_func` hooks are applied correctly.
- `FormMixin` is used with `DetailView` to allow the same URL to both display the object and receive a form POST. This is a clear composition pattern that avoids a separate `CommentCreateView` URL.

## Tradeoffs: FBV vs CBV

- Readability:
  - FBV: explicit step-by-step logic is easy to follow for simple flows.
  - CBV: reduces boilerplate for common patterns (create, update, detail) but requires familiarity with framework hooks.

- Reuse and composition:
  - CBV: mixins enable reusing authentication/authorization (`LoginRequiredMixin`, `UserPassesTestMixin`) and behavior (`FormMixin`) across views.
  - FBV: reuse typically requires helper functions and decorators; composition isn't as structured.

- Extensibility:
  - CBV: easy to override small parts (`form_valid`, `get_context_data`) to extend behavior.
  - FBV: easier for very custom control flows but may lead to duplicated code.

- Testing:
  - Both are testable; CBVs expose hooks that can be unit-tested at the method level.

## Where to look in the code

- `blog/views.py` — main CBV implementations and explanatory docstrings.
- `blog/urls.py` — routes pointing to `PostCreateView`, `PostUpdateView`, `PostDeleteView`, and `PostDetailView`.
- `blog/templates/blog/*` — templates used by the CBVs (`post_form.html`, `post_confirm_delete.html`, `detail.html`).

## Suggested next steps

- Add unit tests that assert ownership checks (edit/delete are allowed only for owners).
- Add messages (Django messages framework) to provide user feedback on create/update/delete success.
- Extract authorization logic into a small `OwnerRequiredMixin` if multiple models will require the same check.

