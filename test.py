for i in range(7, 18):
    print(f'''{{
        "model": "main_app.staff",
        "pk": {i-4},
        "fields": {{
            "department": 1,
            "user": {i},  # Adjusting user IDs by adding 3
            "faculty_id": "{i}",
            "phone_number": 9962526764,
            "resume": "staff/resume/filter{i}_resume.pdf",
            "qualification": "ME , PhD",
            "experience": "{i * 2 + 1} years as a Cyber crime analyst."
        }}
    }},''')