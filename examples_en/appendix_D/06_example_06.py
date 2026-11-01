# Appendix D. Code Recipes – example 6 (manuscript: 93-appendix-d.md, line 90)
usage = None
for chunk in client.models.generate_content_stream(
    model="gemini-3.8-flash",
    contents="Explain to a driver how to fill in a consignment note (TTN) for a groupage shipment.",
):
    if chunk.text:                           # a service chunk may have no text
        print(chunk.text, end="", flush=True)
    usage = chunk.usage_metadata or usage    # usage is reported in the last chunks
print("\noutput tokens:", usage.candidates_token_count if usage else "?")
