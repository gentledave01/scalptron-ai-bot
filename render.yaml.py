services:
  - type: web
    name: scalptron-ai
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python bot.py"
    envVars:
      - key: BOT_TOKEN
        value: 8198909852:AAEbbVLOBLiHJb8TcjPjJNcCHocUExzn44A
