# Appendix D. Code Recipes – example 39 (manuscript: 93-appendix-d.md, line 799)
from google.genai import errors

try:
    resp = client.models.generate_content(model="gemini-3.8-flash", contents="Hello!")
except errors.ClientError as e:                  # 4xx
    if e.code != 429:
        raise                                    # an error in the request, a retry will not help
    print("quota exhausted, retry with a delay:", e.message)
except errors.ServerError as e:                  # 5xx
    print("temporary server failure:", e.code, e.status)
