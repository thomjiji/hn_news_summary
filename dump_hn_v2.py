import json
import requests
import argparse
import html


def extract_text(data):
    texts = []
    if "text" in data and data["text"]:
        texts.append(html.unescape(data["text"]))

    if "children" in data:
        for child in data["children"]:
            texts.extend(extract_text(child))

    return texts


def fetch_and_save_text(post_id):
    api_url = f"https://hn.algolia.com/api/v1/items/{post_id}"

    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            data = json.loads(response.text)

            # Extract texts
            texts = extract_text(data)

            # Create filename, use the post's title, replace spaces with underscores and
            # lowercase all the letters
            title = data.get("title") or "Untitled"
            filename = title.replace(" ", "_").lower()

            # Append post_id to filename
            filename = f"output/txt/{filename}_{post_id}.txt"

            # Write the texts to a txt file
            with open(filename, "w") as f:
                for text in texts:
                    f.write(text + "\n")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON:\n{e}")

    else:
        print(
            f"Error retrieving post data from API, status code: {response.status_code}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch comments from Hacker News post."
    )
    parser.add_argument("post_id", type=int, help="The id of the Hacker News post")

    args = parser.parse_args()

    fetch_and_save_text(args.post_id)
