import fitz  # PyMuPDF
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse,StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import Dashboard


genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

def extract_text_from_pdf(file_path):
    try:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"

def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

@csrf_exempt
def ai_filter(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

    def stream():
        try:
            all_candidates = list(Dashboard.objects.all())
            total = len(all_candidates)
            batch_size = 5
            deleted_count = 0

            for batch_num, batch in enumerate(chunk_list(all_candidates, batch_size)):
                prompt = " You are an expert evaluator. Below is a list of CVs with their corresponding fields. For each, respond with YES or NO only based on the relevance of the CV content to the field.\n\n"
                cv_map = {}

                for i, person in enumerate(batch):
                    content = extract_text_from_pdf(person.cv.path)
                    if content.startswith("ERROR"):
                        continue
                    key = f"CANDIDATE_{i}"
                    cv_map[key] = person
                    prompt += f"\n### {key}\nCV:\n{content[:2000]}\nField: {person.fields}\n"

                prompt += "Now respond YES/NO...\n"
                response = model.generate_content(prompt)
                lines = response.text.strip().splitlines()

                for line in lines:
                    if ':' in line:
                        tag, decision = line.strip().split(':')
                        if decision.strip().upper() == "NO" and tag in cv_map:
                            cv_map[tag].delete()
                            deleted_count += 1

                yield f"PROGRESS: {min((batch_num + 1) * batch_size, total)} of {total} finished\n"

        except Exception as e:
            yield f"PROGRESS: ❌ Error occurred: {str(e)}\n"

    return StreamingHttpResponse(stream(), content_type='text/plain')

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    try:
        all_candidates = list(Dashboard.objects.all())
        deleted_count = 0
        batch_size = 5  

        for batch in chunk_list(all_candidates, batch_size):
            prompt = "You are an expert evaluator. Below is a list of CVs with their corresponding fields. For each, respond with YES or NO only based on the relevance of the CV content to the field.\n\n"

            cv_map = {}
            for i, person in enumerate(batch):
                content = extract_text_from_pdf(person.cv.path)
                if content.startswith("ERROR"):
                    continue  # skip unreadable PDFs
                key = f"CANDIDATE_{i}"
                cv_map[key] = person
                prompt += f"### {key}\nCV:\n{content[:2000]}\nField: {person.fields}\n\n"

            prompt += "Now return only one line for each candidate, format: CANDIDATE_X: YES/NO\n"

            response = model.generate_content(prompt)
            lines = response.text.strip().splitlines()

            for line in lines:
                if ':' in line:
                    tag, decision = line.strip().split(':')
                    decision = decision.strip().upper()
                    if decision == "NO" and tag in cv_map:
                        cv_map[tag].delete()
                        deleted_count += 1

        return redirect('AdminDashboard:admin_dashboard')

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)