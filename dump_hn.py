import requests
import argparse
import html


def fetch_hn_conversation(post_id):
    # HN Algolia API endpoint for item details
    api_url = f"https://hn.algolia.com/api/v1/items/{post_id}"

    # Make a GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()

        # Extract the comments from the response
        comments: list[dict] = data.get("children", [])

        # Extract comment text from the recursive JSON structure
        comment_texts = [
            html.unescape(comment.replace("<p>", ""))
            for comment in recursive_extract_text(comments)
        ]

        # Get the title of the original Hacker News post
        title = data.get("title", "Untitled")

        # Replace spaces with underscores and convert to lowercase
        title = title.replace(" ", "_").lower()

        # Generate the output file name using the modified title
        output_file_name = f"output/{title}.txt"

        # Write the comment texts to the generated output file
        with open(output_file_name, "wb") as file:
            file.write("\n".join(comment_texts).encode("utf-8"))

        print(f"Comment texts saved to {output_file_name}")

    else:
        # Print an error message if the request was not successful
        print(
            f"Error: Unable to fetch conversation. Status Code: {response.status_code}"
        )


def recursive_extract_text(comments: list[dict]) -> list[str]:
    """
    Recursively extracts the text from the comments.

    Args:
        comments: A list of comments.

    Returns:
        A list of comment texts.
    """
    result = []
    for comment in comments:
        if "text" in comment:
            result.append(comment["text"])
        elif "children" in comment:
            result.extend(recursive_extract_text(comment["children"]))
    return result


def extract_comments_keep_hierarchy(data: dict, indent=0):
    if isinstance(data, dict):
        if "text" in data and data["text"] is not None:
            with open("test_output.txt", "a") as f:
                f.write(" " * indent + data["text"] + "\n")
        if "children" in data:
            for child in data["children"]:
                extract_comments_keep_hierarchy(child, indent + 4)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Hacker News conversation and save comment texts to a file."
    )
    parser.add_argument("post_id", type=str, help="Hacker News post ID to fetch")

    args = parser.parse_args()

    fetch_hn_conversation(args.post_id)


if __name__ == "__main__":
    main()