import requests
import openai
from langchain.complexity import LangComplexity

# Set up GitHub API authentication
headers = {
    'Authorization': 'Bearer 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'
}

# Set up OpenAI API key
openai.api_key = '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'

def fetch_repositories(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url, headers=headers)
    repos = response.json()
    return repos

def calculate_complexity(text):
    complexity_score = LangComplexity(text).calculate()
    return complexity_score

def find_most_challenging_repository(username):
    repos = fetch_repositories(username)
    most_challenging_repo = None
    max_complexity_score = -1

    for repo in repos:
        repo_name = repo['name']
        repo_url = repo['html_url']
        response = requests.get(repo['url'], headers=headers)
        repo_data = response.json()
        readme_content = repo_data['readme']['content']

        # Use GPT model to generate repository description
        gpt_response = openai.Completion.create(
            engine='davinci-codex',
            prompt=f'Generate description for {repo_name} repository',
            max_tokens=100,
            temperature=0.7
        )
        generated_description = gpt_response.choices[0].text.strip()

        # Calculate complexity score for the generated description and readme content
        complexity_score = calculate_complexity(generated_description) + calculate_complexity(readme_content)

        if complexity_score > max_complexity_score:
            max_complexity_score = complexity_score
            most_challenging_repo = {
                'name': repo_name,
                'url': repo_url,
                'complexity_score': complexity_score
            }

    return most_challenging_repo

# Get GitHub username from user
username = input("Enter the GitHub username: ")

# Find the most challenging repository
most_challenging_repo = find_most_challenging_repository(username)

if most_challenging_repo:
    print("Most Challenging Repository:")
    print(f"Name: {most_challenging_repo['name']}")
    print(f"URL: {most_challenging_repo['url']}")
    print(f"Complexity Score: {most_challenging_repo['complexity_score']}")
else:
    print("No repositories found for the given username.")
