from flask import Flask, render_template, request, redirect, url_for, flash
import datetime

app = Flask(__name__)

app.secret_key = "any_random_string_you_want_12345"
# --- CUSTOM JINJA FILTER ---
@app.template_filter('strip')
def strip_filter(s):

    if s is not None:
        return s.strip()
    return ""


upcoming_2026 = [
    # WINTER RELEASES (AIRING NOW)
    {"name": "Jujutsu Kaisen (Season 3)", "date": "Jan 8, 2026", "status": "Premiered!", "site": "https://jujutsukaisen.jp/"},
    {"name": "Hell’s Paradise (Season 2)", "date": "Jan 11, 2026", "status": "This Sunday", "site": "https://jigokuraku.com/"},
    {"name": "Oshi no Ko (Season 3)", "date": "Jan 14, 2026", "status": "Next Week", "site": "https://ichigoproduction.com/"},
    {"name": "Frieren (Season 2)", "date": "Jan 16, 2026", "status": "Next Week", "site": "https://frieren-anime.jp/"},

    # SPRING RELEASES
    {"name": "Mushoku Tensei (Season 3)", "date": "April 2026", "status": "Spring", "site": "https://mushokutensei.jp/"},
    {"name": "Slime (Season 4)", "date": "April 2026", "status": "Spring", "site": "https://ten-sura.com/"},
    {"name": "Re:Zero (Season 4)", "date": "April 2026", "status": "Spring", "site": "https://re-zero-anime.jp/"},

    # SUMMER & BEYOND
    {"name": "Bleach: TYBW (Part 4)", "date": "July 2026", "status": "Official Finale", "site": "https://bleach-anime.com/"},
    {"name": "Blue Lock (Season 3)", "date": "Summer 2026", "status": "Summer", "site": "https://bluelock-pr.com/"},
    {"name": "One-Punch Man (S3)", "date": "Mid-2026", "status": "Confirmed", "site": "https://onepunchman-anime.net/"},
    {"name": "Black Clover (Season 2)", "date": "Late 2026", "status": "Confirmed", "site": "https://bclover.jp/"},
    {"name": "Chainsaw Man (S2)", "date": "2026", "status": "TBA", "site": "https://chainsawman.dog/"}
]
# --- DATA DEFINITION ---
ANIME_DATA = [
    {'title': 'Akame ga Kill!', 'year': 2014, 'main_character': 'Akame', 'genres': 'Action, Dark Fantasy, Drama'},
    {'title': 'Attack on Titan', 'year': 2013, 'main_character': 'Eren Yeager',
     'genres': 'Action, Dark Fantasy, Post-apocalyptic'},
    {'title': 'Apothecary Diaries', 'year': 2024, 'main_character': 'Mau-mau', 'genres': 'Romance , Drama '},
    {'title': 'Bleach', 'year': 2004, 'main_character': 'Ichigo Kurosaki', 'genres': 'Action, Supernatural, Adventure'},
    {'title': 'Blue Exorcist', 'year': 2011, 'main_character': 'Rin Okumura',
     'genres': 'Action, Supernatural, Fantasy'},
    {'title': 'Code Geass', 'year': 2006, 'main_character': 'Lelouch Lamperouge', 'genres': 'Mecha, Military, Drama'},
    {'title': 'Dandadan', 'year': 2025, 'main_character': 'Ken Takakura', 'genres': 'Supernatural, Comedy, Action'},
    {'title': 'Death Note', 'year': 2006, 'main_character': 'Light Yagami',
     'genres': 'Psychological Thriller, Supernatural, Mystery'},
    {'title': 'Demon Slayer', 'year': 2019, 'main_character': 'Tanjiro Kamado',
     'genres': 'Action, Dark Fantasy, Adventure'},
    {'title': 'Dragon Ball Z', 'year': 1989, 'main_character': 'Goku', 'genres': 'Action, Martial Arts, Adventure'},
    {'title': 'Dress up darling', 'year': 2018, 'main_character': 'Gojou', 'genres': 'Romance, Fashion, Drama'},
    {'title': 'Fairy Tail', 'year': 2009, 'main_character': 'Natsu Dragneel', 'genres': 'Action, Adventure, Fantasy'},
    {'title': 'Frieren: Beyond Journey’s End', 'year': 2023, 'main_character': 'Frieren',
     'genres': 'Fantasy, Drama, Adventure'},
    {'title': 'Fullmetal Alchemist: Brotherhood', 'year': 2009, 'main_character': 'Edward Elric',
     'genres': 'Action, Adventure, Dark Fantasy'},
    {'title': 'Gachiakuta', 'year': 2025, 'main_character': 'Rudo', 'genres': 'Action, Supernatural'},
    {'title': 'Gintama', 'year': 2006, 'main_character': 'Gintoki Sakata', 'genres': 'Comedy, Action, Parody'},
    {'title': 'Haikyuu!!', 'year': 2014, 'main_character': 'Shoyo Hinata', 'genres': 'Sports, Comedy, Drama'},
    {'title': 'High school of the Dead', 'year': 2006, 'main_character': 'Takashi', 'genres': 'Ecchi, Supernatural'},
    {'title': 'Hunter x Hunter', 'year': 2011, 'main_character': 'Gon Freecss', 'genres': 'Action, Adventure, Fantasy'},
    {'title': 'Jujutsu Kaisen', 'year': 2020, 'main_character': 'Yuji Itadori',
     'genres': 'Action, Dark Fantasy, Supernatural'},
    {'title': 'Kaiju No. 8', 'year': 2025, 'main_character': 'Kafka Hibino', 'genres': 'Action, Sci-Fi, Fantasy'},
    {'title': 'KonoSuba', 'year': 2016, 'main_character': 'Kazuma Satou', 'genres': 'Comedy, Fantasy, Isekai'},
    {'title': 'Lord of the Mysteries', 'year': 2025, 'main_character': 'Klein Moretti', 'genres': 'Mystery, Fantasy, Supernatural', },
    {'title': 'Made in Abyss', 'year': 2017, 'main_character': 'Riko', 'genres': 'Adventure, Dark Fantasy, Drama'},
    {'title': 'Masamune-kun\'s Revenge', 'year': 2017, 'main_character': 'Masamune Makabe',
     'genres': 'Romantic Comedy, Slice of Life'},
    {'title': 'Mob Psycho 100', 'year': 2016, 'main_character': 'Shigeo "Mob" Kageyama',
     'genres': 'Action, Comedy, Supernatural'},
    {'title': 'My Hero Academia', 'year': 2016, 'main_character': 'Izuku Midoriya',
     'genres': 'Action, Superhero, Coming-of-age'},
    {'title': 'Naruto', 'year': 2002, 'main_character': 'Naruto Uzumaki', 'genres': 'Action, Adventure, Coming-of-age'},
    {'title': 'Neon Genesis Evangelion', 'year': 1995, 'main_character': 'Shinji Ikari',
     'genres': 'Mecha, Psychological, Drama'},
    {'title': 'One Piece', 'year': 1999, 'main_character': 'Monkey D. Luffy', 'genres': 'Action, Adventure, Fantasy'},
    {'title': 'One Punch Man', 'year': 2015, 'main_character': 'Saitama', 'genres': 'Action, Comedy, Superhero'},
    {'title': 'Parasyte: The Maxim', 'year': 2014, 'main_character': 'Shinichi Izumi',
     'genres': 'Horror, Sci-Fi, Action'},
    {'title': 'Pokemon', 'year': 1997, 'main_character': 'Ash Ketchum', 'genres': 'Adventure, Fantasy, Family'},
    {'title': 'Re:Zero', 'year': 2016, 'main_character': 'Subaru Natsuki', 'genres': 'Fantasy, Isekai, Drama'},
    {'title': 'Sakamoto Days', 'year': 2025, 'main_character': 'Taro Sakamoto', 'genres': 'Action, Comedy'},
    {'title': 'Sailor Moon', 'year': 1992, 'main_character': 'Usagi Tsukino',
     'genres': 'Magical Girl, Romance, Fantasy'},
    {'title': 'Samurai Champloo', 'year': 2004, 'main_character': 'Mugen & Jin',
     'genres': 'Action, Historical, Adventure'},
    {'title': 'Sentenced to be a hero', 'year': 2026, 'main_character': 'Xylo Forbartz', 'genres': 'Dark fantasy'},
    {'title': 'Solo Leveling', 'year': 2024, 'main_character': 'Sung Jin-Woo', 'genres': 'Action, Fantasy, Adventure'},
    {'title': 'Spy x Family', 'year': 2022, 'main_character': 'Loid Forger', 'genres': 'Comedy, Action, Slice of Life'},
    {'title': 'Steins;Gate', 'year': 2011, 'main_character': 'Rintarou Okabe', 'genres': 'Sci-Fi, Thriller, Drama'},
    {'title': 'The Summer Hikaru Died', 'year': 2025, 'main_character': 'Yoshiki',
     'genres': 'Psychological Thriller, Supernatural, Horror'},
    {'title': 'Tokyo Ghoul', 'year': 2014, 'main_character': 'Kaneki Ken', 'genres': 'Dark Fantasy, Horror, Action'},
    {'title': 'Tougen Anki', 'year': 2025, 'main_character': 'Shiki Ichinose',
     'genres': 'Action, Dark Fantasy, Supernatural'},
    {'title': 'Toradora!', 'year': 2008, 'main_character': 'Ryuuji Takasu', 'genres': 'Romantic Comedy, Slice of Life'},
    {'title': 'Trigun', 'year': 1998, 'main_character': 'Vash the Stampede', 'genres': 'Action, Sci-Fi, Western'},
    {'title': 'Vinland Saga', 'year': 2019, 'main_character': 'Thorfinn', 'genres': 'Historical, Action, Drama'},
    {'title': 'Blue Lock', 'year': 2022, 'main_character': 'Isagi Yoichi', 'genres': 'Sports, Thriller'},
    {'title': 'Chainsaw Man', 'year': 2022, 'main_character': 'Denji', 'genres': 'Action, Dark Fantasy, Gore'},
    {'title': 'Oshi no Ko', 'year': 2023, 'main_character': 'Aqua Hoshino', 'genres': 'Drama, Mystery, Supernatural'},
    {'title': 'Hell’s Paradise', 'year': 2023, 'main_character': 'Gabimaru', 'genres': 'Action, Adventure, Fantasy'},
    {'title': 'Mashle: Magic and Muscles', 'year': 2023, 'main_character': 'Mash Burnedead', 'genres': 'Comedy, Fantasy, Action'},
    {'title': 'Black Clover', 'year': 2017, 'main_character': 'Asta', 'genres': 'Action, Fantasy, Adventure'},
    {'title': 'Cyberpunk: Edgerunners', 'year': 2022, 'main_character': 'David Martinez', 'genres': 'Sci-Fi, Action, Cyberpunk'},
    {'title': 'The Eminence in Shadow', 'year': 2022, 'main_character': 'Cid Kagenou', 'genres': 'Action, Comedy, Fantasy'},
    {'title': 'Wind Breaker', 'year': 2024, 'main_character': 'Haruka Sakura', 'genres': 'Action, Delinquent'},
    {'title': 'Record of Ragnarok', 'year': 2017, 'main_character': 'Brunhilde', 'genres': 'Adventure, Dark fantasy, Martial arts'},
]


@app.route("/")
def home():
    return render_template("index.html", year=datetime.datetime.now().year,upcoming_2026=upcoming_2026)

categories_data = {
    "Anime of the Year": [
        {"year": 2025, "winner": "Solo Leveling"},
        {"year": 2024, "winner": "Jujutsu Kaisen S2"},
        {"year": 2023, "winner": "Cyberpunk: Edgerunners"},
        {"year": 2022, "winner": "Attack on Titan Final Season Pt 1"},
        {"year": 2021, "winner": "Jujutsu Kaisen"},
        {"year": 2017, "winner": "Yuri!!! on Ice"},
        {"year": 2014, "winner": "Attack on Titan (TAAF)"},
        {"year": 2012, "winner": "Madoka Magica (TAAF)"}
    ],
    "Best Animation": [
        {"year": 2025, "winner": "Demon Slayer: Hashira Training Arc"},
        {"year": 2024, "winner": "Demon Slayer: Swordsmith Village Arc"},
        {"year": 2022, "winner": "Demon Slayer: Mugen Train Arc"},
        {"year": 2020, "winner": "Mob Psycho 100 II"},
        {"year": 2019, "winner": "Violet Evergarden"},
        {"year": 2016, "winner": "One Punch Man (Fans' Choice)"}
    ],
    "Best Drama": [
        {"year": 2025, "winner": "Frieren: Beyond Journey's End"},
        {"year": 2024, "winner": "Attack on Titan Final Chapters Special 1"},
        {"year": 2021, "winner": "Fruits Basket Season 2"},
        {"year": 2020, "winner": "Vinland Saga"},
        {"year": 2017, "winner": "Erased"}
    ],
    "Best Film": [
        {"year": 2025, "winner": "Look Back"},
        {"year": 2024, "winner": "Suzume"},
        {"year": 2023, "winner": "Jujutsu Kaisen 0"},
        {"year": 2022, "winner": "Demon Slayer: Mugen Train Movie"},
        {"year": 2018, "winner": "Your Name"},
        {"year": 2010, "winner": "Summer Wars (TAAF)"}
    ]}
@app.route("/blog")
def blog():
    # Sort data so newest years appear first
    return render_template('blog.html', categories=categories_data)

@app.route("/anime")
def anime():
    query = request.args.get('query', '').lower().strip()
    if query:
        filtered_data = [a for a in ANIME_DATA if query in a['title'].lower()]
        return render_template("anime.html", anime_data=filtered_data, search_term=query, date=2026)
    return render_template("anime.html", anime_data=ANIME_DATA, date=2026)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if not query:
        return redirect(url_for('anime'))

    match_exists = any(query.lower() in a['title'].lower() for a in ANIME_DATA)

    if match_exists:
        # Redirect to the anime list with the query as a parameter
        return redirect(url_for('anime', query=query))
    else:
        # Flash message stays for ONE load, then disappears on refresh
        flash(f"Not Found. Check full site for: {query}")
        return redirect(url_for('home'))
if __name__ == "__main__":
    app.run(debug=True)