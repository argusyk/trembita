# Appendix D. Code Recipes – example 3 (manuscript: 93-appendix-d.md, line 37)
cloud_client = genai.Client(
    vertexai=True,                   # new name of the same flag: enterprise=True
    project="smereka-trembita",
    location="europe-west4",
)
