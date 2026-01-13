import requests
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
    {"name": "Hell’s Paradise (Season 2)", "date": "Jan 11, 2026", "status": "Premiered!", "site": "https://jigokuraku.com/"},
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
    {"name": "Chainsaw Man (S2)", "date": "2026", "status": "TBA", "site": "https://chainsawman.dog/"},
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
    {'title': 'Blue lock', 'year': 2022, 'main_character': 'Isagi Yoichi', 'genres': 'Sports, Thriller'},
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


@app.route("/info")
def info():
    # Sort data so newest years appear first
    return render_template('info.html')


def get_anime_details(anime_id):
    # Fetch Staff Info
    staff_res = requests.get(f"https://api.jikan.moe/v4/anime/{anime_id},/staff")
    # Fetch User Reviews
    review_res = requests.get(f"https://api.jikan.moe/v4/anime/{anime_id},/reviews")

    staff = staff_res.json().get('data', [])[:5]  # Top 5 staff members
    reviews = review_res.json().get('data', [])[:3]  # Top 3 fan reviews

    return staff, reviews


@app.route('/blog')
@app.route('/blog')
def blog():
    epic_scenes = [
        {
            "title": "Attack on Titan",
            "tag": "Action, Dark Fantasy",
            "moment": "Eren transforms into a Titan in front of everyone during the Battle of Trost, shocking both characters and viewers.",
             "episode": "Episode8",
            "impact": "Established one of the most adrenaline-pumping sequences in recent anime."
        },
        {
            "title": "Demon Slayer",
            "tag": "Action, Supernatural",
            "moment": "Tanjiro uses the Hinokami Kagura (Dance of the Fire God) to save Nezuko from Rui's threads.",
             "episode": "Episode 19",
            "impact": "A visual masterclass that redefined the standard for modern shonen animation."
        },
        {
            "title": "Your Name",
            "tag": "Romance, Supernatural",
            "moment": "Taki and Mitsuha finally meet on the mountainside during twilight, only to forget each other's names as sun sets.",
            "episode":  "Feature Film",
            "impact": "Created a globally recognized 'heartbreak' moment that transcends language barriers."
        },
        {
            "title": "Naruto Shippuden",
            "tag": "Action, Fantasy",
            "moment": "Naruto arrives in Sage Mode on top of a giant toad to face Pain in the ruins of the Hidden Leaf.",
             "episode": "Episode 163",
            "impact": "The ultimate 'hero's return' that cemented Naruto's legacy as the village's protector."
        },
        {
            "title": "Toradora!",
            "tag": "Romance, Slice of Life",
            "moment": "Taiga breaks down in the street, realizing her true feelings for Ryuuji after he leaves her apartment.",
             "episode": "Episode 19",
            "impact": "Commonly cited as one of the most raw and emotional 'Christmas Eve' moments in anime history."
        },



    {
        "title": "Attack on Titan",
        "tag": "Action, Dark Fantasy",
        "moment": "Eren transforms into a Titan in front of everyone during the Battle of Trost, shocking both characters and viewers",
         "episode": "Episode 8",
        "impact": "Established one of the most adrenaline-pumping sequences in recent anime"
    },
    {
        "title": "My Hero Academia",
        "tag": "Action, Superhero",
        "moment": "Midoriya and Bakugo finally team up against Overhaul, showcasing a powerful hero vs villain showdown",
         "episode": "Episode 13, Season 4",
        "impact": "Epic fight scene with intense animations and emotional character development"
    },
    {
        "title": "Naruto Shippuden",
        "tag": "Action, Shonen",
        "moment": "Naruto unleashes Kurama’s full power to save comrades during the Pain arc",
         "episode": "Episode 163",
        "impact": "Iconic power-up moment that defines Naruto’s growth and determination"
    },
    {
        "title": "One Piece",
        "tag": "Adventure, Action",
        "moment": "Luffy declares war on the World Government following Ace’s death in Marineford, motivating thousands",
         "episode": "Episode 505",
        "impact": "A pivotal character moment with massive emotional resonance and hype factor"
    },
        {
            "title": "Steins;Gate",
            "tag": "Sci-Fi, Thriller",
            "moment": "Okabe finally saves Mayuri from a time-loop death scenario, delivering high tension and emotional payoff",
             "episode": "Episode 22-23",
            "impact": "Emotional climax and critical plot twist, widely regarded as one of the most intense anime moments"
        },
        {
            "title": "Attack on Titan",
            "tag": "Action, Dark Fantasy",
            "moment": "Eren transforms into a Titan in front of everyone during the Battle of Trost, shocking both characters and viewers",
             "episode": "Episode 8",
            "impact": "Established one of the most adrenaline-pumping sequences in recent anime"
        },
        {
            "title": "My Hero Academia",
            "tag": "Action, Superhero",
            "moment": "Midoriya and Bakugo finally team up against Overhaul, showcasing a powerful hero vs villain showdown",
             "episode": "Episode 13, Season 4",
            "impact": "Epic fight scene with intense animations and emotional character development"
        },
        {
            "title": "Naruto Shippuden",
            "tag": "Action, Shonen",
            "moment": "Naruto unleashes Kurama’s full power to save comrades during the Pain arc",
             "episode": "Episode 163",
            "impact": "Iconic power-up moment that defines Naruto’s growth and determination"
        },
        {"title": "Dorohedoro", "tag": "Action, Dark Fantasy, Mystery", "episode":" Episode 12",
         "impact": "Proved that 3D-CGI can perfectly capture gritty, surrealist art styles.",
         "moment": "Caiman uncovers the sorcerer responsible for his reptile head in a chaotic, bloody showdown."},

        {"title": "Vivy: Fluorite Eye's Song", "tag": "Sci-Fi, Music, Action", "episode":" Episode 13",
         "impact": "A landmark for original sci-fi, blending high-stakes AI ethics with idol culture.",
         "moment": "Vivy defies time to prevent a catastrophic war between humans and AI with a breathtaking musical battle."},

        {"title": "Demon Slayer: Kimetsu no Yaiba", "tag": "Action, Supernatural, Dark Fantasy", "episode":" Episode 63",
         "impact": "Reshaped the global anime market; broke box office records worldwide.",
         "moment": "Tanjiro and Nezuko fight Upper-Rank demons in a high-stakes, visually stunning battle with sword and fire techniques."},

        {"title": "Metallic Rouge", "tag": "Sci-Fi, Mecha, Action", "episode":" Episode 13",
         "impact": "A stylish homage to classic 90s tech-noir, celebrating Studio Bones' 25th anniversary.",
         "moment": "Rouge confronts the Immortal Nine with her bio-mechanic suit, challenging the limits of human and android cooperation."},

        {"title": "Shadows House", "tag": "Mystery, Psychological, Supernatural", "episode":" Episode 25",
         "impact": "Revitalized the 'Gothic Mystery' sub-genre with a unique focus on class and identity.",
         "moment": "Emilico uncovers the grotesque truth behind the masters and the living dolls, revealing the mansion's dark secrets."},

        {"title": "Parasyte: The Maxim", "tag": "Horror, Sci-Fi, Action", "episode":" Episode 24",
         "impact": "A definitive masterpiece of biological horror that questions the definition of humanity.",
         "moment": "Shinichi and Migi face a ruthless Parasyte, blending body horror with an ethical dilemma of coexistence."},

        {"title": "Akame ga Kill!", "tag": "Action, Adventure, Dark Fantasy", "episode":" Episode 24",
         "impact": "Famous for its brutal subversion of 'plot armor' in the shonen genre.",
         "moment": "Tatsumi participates in a high-stakes battle against the Imperial forces alongside Akame, showcasing sword combat and revenge plots."},

        {"title": "Jujutsu Kaisen", "tag": "Action, Supernatural, Shōnen", "episode":" Episode 47",
         "impact": "The current face of modern shonen, leading the 'Dark Trio' of the 2020s.",
         "moment": "Yuji Itadori battles cursed spirits using Sukuna’s transformative powers in intense, perfectly choreographed sequences."},

        {"title": "Kaiju No. 8", "tag": "Action, Sci-Fi, Shōnen", "episode":" Episode 12",
         "impact": "Bridged the gap between traditional monster movies and modern battle manga.",
         "moment": "Kafka Hibino undergoes a transformation into a kaiju while fighting giant monsters, balancing humor and adrenaline."},

        {"title": "Chainsaw Man", "tag": "Horror, Action, Dark Fantasy", "episode":" Episode 12",
         "impact": "Changed the industry's approach to cinematic directing and gritty, realistic sound design.",
         "moment": "Denji confronts massive devils with his chainsaw transformations, blending gore and high-paced action."},

        {"title": "The Promised Neverland", "tag": "Thriller, Mystery, Horror", "episode":" Episode 23",
         "impact": "Set a new standard for psychological suspense and high-stakes 'prison break' narratives.",
         "moment": "Emma, Norman, and Ray escape from a demon-operated orphanage after uncovering its horrifying truth."},

        {"title": "Deca-Dence", "tag": "Sci-Fi, Post-Apocalyptic, Action", "episode":" Episode 12",
         "impact": "Praised for its bold mid-series twist that flipped the entire worldbuilding on its head.",
         "moment": "Natsume discovers that the post-apocalyptic world is a simulated reality controlled by an elite society."},

        {"title": "Gargantia on the Verdurous Planet", "tag": "Sci-Fi, Adventure, Mecha", "episode":" Episode 13",
         "impact": "Offered a profound philosophical look at peaceful coexistence vs. total war.",
         "moment": "Ledo crash-lands on Earth and must adapt while defending humans against Hideauze monsters with robot combat."},

        {"title": "No. 6", "tag": "Sci-Fi, Dystopia, Mystery", "episode":" Episode 11",
         "impact": "A core title for fans of dystopian social commentary and deep character bonds.",
         "moment": "Shion and Nezumi uncover shocking truths about the city-state's government and its manipulative secrets."},

        {"title": "Ergo Proxy", "tag": "Psychological, Sci-Fi, Mystery", "episode":" Episode 23",
         "impact": "A pillar of philosophical cyberpunk that challenged viewers' understanding of identity.",
         "moment": "Re-l Mayer confronts the enigmatic Proxy, revealing existential truths about humanity and self-awareness."},

        {"title": "Land of the Lustrous", "tag": "Fantasy, Adventure, Sci-Fi", "episode":" Episode 12",
         "impact": "Widely considered the most visually innovative use of 3D-CGI in anime history.",
         "moment": "Phosphophyllite uncovers the Lunarians' motives while defending brittle gemstone beings, reflecting survival and identity."},

        {"title": "God Eater", "tag": "Action, Sci-Fi, Post-Apocalyptic", "episode":" Episode 13",
         "impact": "Showcased Ufotable's early mastery of digital lighting and unique texture mapping.",
         "moment": "Lenka Utsugi confronts monstrous Aragami using God Arcs, combining human skill and bio-engineered powers."},

        {"title": "Kabaneri of the Iron Fortress", "tag": "Action, Steampunk, Horror", "episode":" Episode 12",
         "impact": "A visual powerhouse that combined steampunk aesthetics with high-octane survival horror.",
         "moment": "Ikoma breaches the armored walls fighting the Kabane with his improvised steam gun, echoing titan combat chaos."},

        {"title": "Neon Genesis Evangelion", "tag": "Mecha, Psychological, Sci-Fi", "episode":" Episode 26",
         "impact": "Deconstructed the mecha genre and remains the most influential psychological anime ever.",
         "moment": "Shinji pilots Eva-01 against an enigmatic angel, balancing human trauma and existential threats."},

        {"title": "Re:Zero – Starting Life in Another World", "tag": "Isekai, Psychological, Fantasy", "episode":" Episode 50",
         "impact": "Redefined the Isekai genre by replacing power fantasies with visceral psychological suffering.",
         "moment": "Subaru dies repeatedly to orchestrate a strategy against witches and monsters, uncovering resilience and despair."}
    ]




    return render_template('blog.html', scenes=epic_scenes)
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
        flash(f"Not Found. Check full site for: {query},")
        return redirect(url_for('home'))
if __name__ == "__main__":
    app.run(debug=True)