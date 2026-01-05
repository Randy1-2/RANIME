from flask import Flask, render_template, request, redirect, url_for
import datetime
import re
app = Flask(__name__)

# --- CUSTOM JINJA FILTER ---
def strip_filter(s):
    """Jinja filter to apply the Python strip() method."""
    if s is not None:
        return s.strip()
    return ""

app.jinja_env.filters['strip'] = strip_filter
# -------------------------------------------------

# --- DATA DEFINITION ---
# The ANIME_DATA structure must contain keys: 'title', 'year', 'main_character', 'genres'.
ANIME_DATA = [
    {'title': 'Akame ga Kill!', 'year': 2014, 'main_character': 'Akame', 'genres': 'Action, Dark Fantasy, Drama'},
    {'title': 'Attack on Titan', 'year': 2013, 'main_character': 'Eren Yeager', 'genres': 'Action, Dark Fantasy, Post-apocalyptic'},
    {'title': 'Apothecary Diaries', 'year': 2024, 'main_character': 'Mau-mau', 'genres': 'Romance , Drama '},
    {'title': 'Bleach', 'year': 2004, 'main_character': 'Ichigo Kurosaki', 'genres': 'Action, Supernatural, Adventure'},
    {'title': 'Blue Exorcist', 'year': 2011, 'main_character': 'Rin Okumura', 'genres': 'Action, Supernatural, Fantasy'},
    {'title': 'Code Geass', 'year': 2006, 'main_character': 'Lelouch Lamperouge', 'genres': 'Mecha, Military, Drama'},
    {'title': 'Dandadan', 'year': 2025, 'main_character': 'Ken Takakura', 'genres': 'Supernatural, Comedy, Action'},
    {'title': 'Death Note', 'year': 2006, 'main_character': 'Light Yagami', 'genres': 'Psychological Thriller, Supernatural, Mystery'},
    {'title': 'Demon Slayer', 'year': 2019, 'main_character': 'Tanjiro Kamado', 'genres': 'Action, Dark Fantasy, Adventure'},
    {'title': 'Dragon Ball Z', 'year': 1989, 'main_character': 'Goku', 'genres': 'Action, Martial Arts, Adventure'},
    {'title': 'Dress up darling', 'year': 2018, 'main_character': 'Gojou', 'genres': 'Romance, Fashion, Drama'},
    {'title': 'Fairy Tail', 'year': 2009, 'main_character': 'Natsu Dragneel', 'genres': 'Action, Adventure, Fantasy'},
    {'title': 'Frieren: Beyond Journey’s End', 'year': 2023, 'main_character': 'Frieren', 'genres': 'Fantasy, Drama, Adventure'},
    {'title': 'Fullmetal Alchemist: Brotherhood', 'year': 2009, 'main_character': 'Edward Elric', 'genres': 'Action, Adventure, Dark Fantasy'},
    {'title': 'Gachiakuta', 'year': 2025, 'main_character': 'Rudo', 'genres': 'Action, Supernatural'},
    {'title': 'Gintama', 'year': 2006, 'main_character': 'Gintoki Sakata', 'genres': 'Comedy, Action, Parody'},
    {'title': 'Haikyuu!!', 'year': 2014, 'main_character': 'Shoyo Hinata', 'genres': 'Sports, Comedy, Drama'},
    {'title': 'High school of the Dead', 'year': 2006, 'main_character': 'Takashi', 'genres': 'Ecchi, Supernatural'},
    {'title': 'Hunter x Hunter', 'year': 2011, 'main_character': 'Gon Freecss', 'genres': 'Action, Adventure, Fantasy'},
    {'title': 'Jujutsu Kaisen', 'year': 2020, 'main_character': 'Yuji Itadori', 'genres': 'Action, Dark Fantasy, Supernatural'},
    {'title': 'Kaiju No. 8', 'year': 2025, 'main_character': 'Kafka Hibino', 'genres': 'Action, Sci-Fi, Fantasy'},
    {'title': 'KonoSuba', 'year': 2016, 'main_character': 'Kazuma Satou', 'genres': 'Comedy, Fantasy, Isekai'},
    {'title': 'Made in Abyss', 'year': 2017, 'main_character': 'Riko', 'genres': 'Adventure, Dark Fantasy, Drama'},
    {'title': 'Masamune-kun\'s Revenge', 'year': 2017, 'main_character': 'Masamune Makabe', 'genres': 'Romantic Comedy, Slice of Life'},
    {'title': 'Mob Psycho 100', 'year': 2016, 'main_character': 'Shigeo "Mob" Kageyama', 'genres': 'Action, Comedy, Supernatural'},
    {'title': 'My Hero Academia', 'year': 2016, 'main_character': 'Izuku Midoriya', 'genres': 'Action, Superhero, Coming-of-age'},
    {'title': 'Naruto', 'year': 2002, 'main_character': 'Naruto Uzumaki', 'genres': 'Action, Adventure, Coming-of-age'},
    {'title': 'Neon Genesis Evangelion', 'year': 1995, 'main_character': 'Shinji Ikari', 'genres': 'Mecha, Psychological, Drama'},
    {'title': 'One Piece', 'year': 1999, 'main_character': 'Monkey D. Luffy', 'genres': 'Action, Adventure, Fantasy'},
    {'title': 'One Punch Man', 'year': 2015, 'main_character': 'Saitama', 'genres': 'Action, Comedy, Superhero'},
    {'title': 'Parasyte: The Maxim', 'year': 2014, 'main_character': 'Shinichi Izumi', 'genres': 'Horror, Sci-Fi, Action'},
    {'title': 'Pokemon', 'year': 1997, 'main_character': 'Ash Ketchum', 'genres': 'Adventure, Fantasy, Family'},
    {'title': 'Re:Zero', 'year': 2016, 'main_character': 'Subaru Natsuki', 'genres': 'Fantasy, Isekai, Drama'},
    {'title': 'Sakamoto Days', 'year': 2025, 'main_character': 'Taro Sakamoto', 'genres': 'Action, Comedy'},
    {'title': 'Sailor Moon', 'year': 1992, 'main_character': 'Usagi Tsukino', 'genres': 'Magical Girl, Romance, Fantasy'},
    {'title': 'Samurai Champloo', 'year': 2004, 'main_character': 'Mugen & Jin', 'genres': 'Action, Historical, Adventure'},
    {'title': 'Solo Leveling', 'year': 2024, 'main_character': 'Sung Jin-Woo', 'genres': 'Action, Fantasy, Adventure'},
    {'title': 'Spy x Family', 'year': 2022, 'main_character': 'Loid Forger', 'genres': 'Comedy, Action, Slice of Life'},
    {'title': 'Steins;Gate', 'year': 2011, 'main_character': 'Rintarou Okabe', 'genres': 'Sci-Fi, Thriller, Drama'},
    {'title': 'The Summer Hikaru Died', 'year': 2025, 'main_character': 'Yoshiki', 'genres': 'Psychological Thriller, Supernatural, Horror'},
    {'title': 'Tokyo Ghoul', 'year': 2014, 'main_character': 'Kaneki Ken', 'genres': 'Dark Fantasy, Horror, Action'},
    {'title': 'Tougen Anki', 'year': 2025, 'main_character': 'Shiki Ichinose', 'genres': 'Action, Dark Fantasy, Supernatural'},
    {'title': 'Toradora!', 'year': 2008, 'main_character': 'Ryuuji Takasu', 'genres': 'Romantic Comedy, Slice of Life'},
    {'title': 'Trigun', 'year': 1998, 'main_character': 'Vash the Stampede', 'genres': 'Action, Sci-Fi, Western'},
    {'title': 'Vinland Saga', 'year': 2019, 'main_character': 'Thorfinn', 'genres': 'Historical, Action, Drama'},
]


# --- HELPER FUNCTION ---
def create_anime_id(title):
    """Generates a highly robust URL-friendly ID slug by matching the Jinja logic."""
    # SANITIZE: Remove most special characters using regex
    sanitized_title = re.sub(r'[^A-Za-z0-9 ]+', '', title)

    # SLUGIFY: Convert to lowercase, replace spaces with hyphens, and strip
    return sanitized_title.lower().replace(' ', '-').strip()


@app.route("/")
def home():
    current_year = datetime.datetime.now().year

    # Pass the current year to index.html
    return render_template("index.html", year=current_year)


@app.route("/anime")
def anime():
    """Renders the anime list table page (anime.html)."""
    current_year = datetime.datetime.now().year
    return render_template("anime.html", date=current_year, anime_data=ANIME_DATA)
@app.route('/search', methods=['GET'])
def search():
    """Handles the search query and redirects or shows errors."""
    search_query = request.args.get('query', '').lower().strip()

    # Case 1: Search bar was empty
    if not search_query:
        return render_template('index.html', error_message="Not Found\nCheck full site")

    # Case 2: Look for a match
    for anime_item in ANIME_DATA:
        if search_query in anime_item['title'].lower():
            anime_id_slug = create_anime_id(anime_item['title'])
            return redirect(url_for('anime', _anchor=anime_id_slug))


    return render_template('index.html', error_message="Not Found\nCheck full site")
@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route('/api/login', methods=['POST'])
def login():
    """Handles the form submission from the login page."""


    if request.method == 'POST':
        # 1. Get data from the form (request.form)
        email = request.form.get('email')
        password = request.form.get('password')
        recaptcha_response = request.form.get('g-recaptcha-response')

    return redirect(url_for('home'))



if __name__=="__main__":
    app.run(debug = True)