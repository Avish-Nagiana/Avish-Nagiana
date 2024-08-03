import requests
import os

USERNAME = os.getenv('GITHUB_USERNAME')
TOKEN = os.getenv('GITHUB_TOKEN')

if not USERNAME or not TOKEN:
    raise ValueError('GitHub username or token environment variables are missing.')

def fetch_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url, auth=(USERNAME, TOKEN))
    response.raise_for_status()
    return response.json()

def fetch_languages(repo_name):
    url = f'https://api.github.com/repos/{USERNAME}/{repo_name}/languages'
    response = requests.get(url, auth=(USERNAME, TOKEN))
    response.raise_for_status()
    return response.json()

def generate_markdown(languages):
    markdown = '## Languages and Tools\n\n'
    for lang, color in languages.items():
        badge_url = f'https://img.shields.io/badge/{lang.replace(" ", "%20")}-000000?style=flat&logo={lang.lower().replace(" ", "-")}&logoColor=white'
        markdown += f'<img src="{badge_url}" alt="{lang}" />\n'
    return markdown

def main():
    repos = fetch_repos(USERNAME)
    language_count = {}
    
    for repo in repos:
        languages = fetch_languages(repo['name'])
        for lang, lines in languages.items():
            if lang in language_count:
                language_count[lang] += lines
            else:
                language_count[lang] = lines
    
    sorted_languages = dict(sorted(language_count.items(), key=lambda item: item[1], reverse=True))
    
    top_languages = {lang: '000000' for lang in sorted_languages.keys()}  # Placeholder color
    markdown = generate_markdown(top_languages)
    
    # Read the current README
    with open('README.md', 'r') as file:
        readme_content = file.read()
    
    # Replace the placeholder section with new content
    updated_content = readme_content.replace('<!-- START_LANGUAGES -->', f'<!-- START_LANGUAGES -->\n{markdown}\n<!-- END_LANGUAGES -->')
    
    # Write the updated README
    with open('README.md', 'w') as file:
        file.write(updated_content)

if __name__ == '__main__':
    main()
