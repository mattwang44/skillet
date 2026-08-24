# Credits

`eli5` is a near-verbatim mirror of the skill by Thariq Shihipar (@trq212),
published under MIT in [anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community/tree/main/eli5).

Only the `description` field differs: the upstream description names the slash
command, this one also lists the natural-language situations that should trigger
it, so it fires without being invoked by name.

The body is left untouched on purpose. It is the reference point for this
repo's taste: the model already knows how to explain things, so the only thing
worth spending tokens on is the output format.
