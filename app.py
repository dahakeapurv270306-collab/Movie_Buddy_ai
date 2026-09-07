import random
import string
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "movie-buddy-secret-key"


def get_response(user_input):
    """Takes raw user text and returns Movie Buddy's reply as a string."""
    clean_input = user_input.lower().strip().translate(
        str.maketrans("", "", string.punctuation)
    )
    words = clean_input.split()

    # GREETING
    if any(w in words for w in ["hello", "hi", "hey"]):
        return random.choice([
            "Hello! What kind of movie are you in the mood for?",
            "Hey, movie lover! Looking for something to watch?",
            "Hi there! Tell me what genre you're craving!"
        ])

    # GOODBYE
    if any(w in words for w in ["bye", "goodbye", "exit", "quit"]):
        return "Goodbye, movie lover! May your next watch become your new favorite."

    # HELP
    if "help" in words:
        return (
            "Movie Buddy can help you with:\n\n"
            "RECOMMENDATIONS\n"
            "- recommend an action movie / comedy / romance / horror / sci-fi\n\n"
            "DIRECTORS\n"
            "- Who is Christopher Nolan? / Who is Steven Spielberg?\n\n"
            "MOVIES\n"
            "- Tell me about Inception / Titanic / The Dark Knight\n\n"
            "OTHER\n"
            "- hello, thanks, bye"
        )

    # THANK YOU
    if "thank" in words or "thanks" in words:
        return random.choice([
            "You're very welcome! Happy watching!",
            "Anytime! May you never run out of good movies.",
            "Happy to help, movie lover!"
        ])

    # ACTION
    if "action" in words:
        return (
            "ACTION RECOMMENDATIONS\n\n"
            "1. The Dark Knight - Christopher Nolan: Batman battles the Joker for Gotham's soul.\n"
            "2. Mad Max: Fury Road - George Miller: A relentless post-apocalyptic chase.\n"
            "3. John Wick - Chad Stahelski: A retired hitman returns for revenge."
        )

    # COMEDY
    if "comedy" in words or "funny" in words:
        return (
            "COMEDY RECOMMENDATIONS\n\n"
            "1. Superbad - Greg Mottola: Two friends' last days before graduation.\n"
            "2. The Grand Budapest Hotel - Wes Anderson: A quirky caper with a legendary concierge.\n"
            "3. Bridesmaids - Paul Feig: Friendship and rivalry amid wedding chaos."
        )

    # ROMANCE
    if "romance" in words or "romantic" in words or "love" in words:
        return (
            "ROMANCE RECOMMENDATIONS\n\n"
            "1. Titanic - James Cameron: A doomed love story aboard the RMS Titanic.\n"
            "2. La La Land - Damien Chazelle: A musical romance in Los Angeles.\n"
            "3. The Notebook - Nick Cassavetes: A love story spanning decades."
        )

    # HORROR / THRILLER
    if "horror" in words or "thriller" in words or "scary" in words:
        return (
            "HORROR & THRILLER RECOMMENDATIONS\n\n"
            "1. Get Out - Jordan Peele: A disturbing secret unravels during a family visit.\n"
            "2. A Quiet Place - John Krasinski: Survival in silence against deadly creatures.\n"
            "3. Se7en - David Fincher: Detectives hunt a killer using the seven deadly sins."
        )

    # SCI-FI / FANTASY
    if "sci-fi" in words or "scifi" in words or "fantasy" in words or "space" in words:
        return (
            "SCI-FI & FANTASY RECOMMENDATIONS\n\n"
            "1. Inception - Christopher Nolan: A thief who steals ideas through dreams.\n"
            "2. Interstellar - Christopher Nolan: Explorers search for humanity's new home.\n"
            "3. The Fellowship of the Ring - Peter Jackson: A hobbit's quest to save Middle-earth."
        )

    # CHRISTOPHER NOLAN
    if "nolan" in words:
        return (
            "CHRISTOPHER NOLAN\n\n"
            "A British-American director known for mind-bending, visually ambitious films "
            "such as Inception, Interstellar, The Dark Knight Trilogy, and Oppenheimer."
        )

    # STEVEN SPIELBERG
    if "spielberg" in words:
        return (
            "STEVEN SPIELBERG\n\n"
            "A pioneer of modern blockbuster filmmaking, known for Jaws, E.T., "
            "Jurassic Park, and Schindler's List."
        )

    # INCEPTION
    if "inception" in clean_input:
        return (
            "INCEPTION\n"
            "Director: Christopher Nolan | Genre: Sci-Fi / Thriller\n\n"
            "Dom Cobb steals secrets from dreams and is offered a chance at redemption "
            "by planting an idea instead of stealing one."
        )

    # TITANIC
    if "titanic" in clean_input:
        return (
            "TITANIC\n"
            "Director: James Cameron | Genre: Romance / Drama\n\n"
            "Jack and Rose fall in love aboard the ill-fated RMS Titanic."
        )

    # THE DARK KNIGHT
    if "dark knight" in clean_input:
        return (
            "THE DARK KNIGHT\n"
            "Director: Christopher Nolan | Genre: Action / Crime\n\n"
            "Batman confronts the Joker's chaos and the line between hero and vigilante."
        )

    # GENERAL MOVIE QUESTION
    if "movie" in words or "movies" in words:
        return (
            "I can help you find your next watch!\n"
            "Try: \"recommend an action movie\", \"suggest a comedy\", \"who is Christopher Nolan\""
        )

    # UNKNOWN INPUT
    return (
        "I'm not quite sure what you mean.\n"
        "Ask about: recommendations, directors, or specific movies.\n"
        "Type 'help' to see examples."
    )


@app.route("/", methods=["GET", "POST"])
def index():
    if "chat" not in session:
        session["chat"] = [
            ("bot", "Hello, movie lover! I'm Movie Buddy, your film assistant. "
                    "Ask me for recommendations, directors, or specific movies. "
                    "Type 'help' anytime.")
        ]

    if request.method == "POST":
        user_message = request.form.get("message", "").strip()
        if user_message:
            chat = session["chat"]  
            chat.append(("user", user_message))
            chat.append(("bot", get_response(user_message)))
            session["chat"] = chat

    return render_template("index.html", chat=session["chat"])


@app.route("/reset", methods=["POST"])
def reset():
    session.pop("chat", None)
    return render_template("index.html", chat=[])


if __name__ == "__main__":
    app.run(debug=True)
