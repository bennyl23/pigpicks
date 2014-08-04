from django.http import HttpResponseRedirect

# REMOVE THIS!!!
from login.models import User

def signed_in_only(function):
    def _decorator(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login')

        return function(request, *args, **kwargs)

    return _decorator

def clear_session(request):
    request.session.clear()

def check_reset_password_access(function):
    def _decorator(request, *args, **kwargs):
        if 'user_id' not in request.session and 'user_id_to_reset' not in request.session:
            return HttpResponseRedirect('/login/session_ended')

        return function(request, *args, **kwargs)

    return _decorator

# REMOVE THIS!!!
def insert_users():
    user_list = [[32, "tmdickson@comcast.net", "TMD24", "goldfever", 0, 1, "T Dix", "E", "Sap", 0],
                [34, "BAGMAN1@COMCAST.NET", "BAGMAN", "RELAX", 0, 1, "DB", "E", "DB", 0],
                [35, "anthonydoucet@hotmail.com", "Yardtown", "oioioi", 0, 1, "TD", "E", "MD", 0],
                [37, "nickstjean15@gmail.com", "Knocker", "intrepid", 0, 1, "N St J", "E", "Kn", 0],
                [42, "sheadiddy40@yahoo.com", "Uno Cinco ", "central", 0, 1, "SN", "E", "Kn", 0],
                [44, "mikefitz1963@gmail.com", "Fitzy", "zzzzz", 0, 1, "M Ftz", "E", "MF", 0],
                [46, "billysbar@comcast.net", "stixs", "zxc9040", 0, 1, "BLab", "E", "BLab", 0],
                [47, "tpflynnjr@yahoo.com", "Chicken Dinner", "school14", 0, 1, "TPFlynn", "E", "Kn", 0],
                [89, "pamsap@yahoo.com", "Toga914", "sappp", 0, 1, "PS", "E", "PS", 0],
                [50, "giampetruzzi@comcast.net", "st.rams", "cg1224", 0, 1, "C G", "E", "E", 0],
                [88, "scrubrub@comcast.net", "Carnac", "scrubrub", 0, 1, "RS", "E", "RS", 0],
                [60, "billlucci@yahoo.com", "breadman", "bread", 0, 1, "BLuc", "E", "BLuc", 0],
                [62, "mtrombly2@mac.com", "Trombly", "mat123", 0, 1, "M Tr", "Ben", "MT", 0],
                [104, "wdflowers@hotmail.com", "Big Shamrock", "cowboy", 0, 1, "WFl", "NPNPNP", "MF", 0],
                [68, "kevin@pawsitivelyweb.com", "tricity", "1qwer5", 0, 1, "K Thom", "E", "KH", 0],
                [77, "dcasey@trivantus.com", "Skidz", "sovereign", 0, 1, "DC", "E", "DC", 0],
                [72, "trentwilly@yahoo.com", "New Money", "booboo00", 0, 1, "IW", "E", "Bal", 0],
                [85, "gapo222@aol.com", "pdiddy", "pools", 0, 1, "BPaq", "E", "BPaq", 0],
                [87, "f-kelley@comcast.net", "ducks", "232323", 0, 1, "FK", "NPNPNP", "MF", 0],
                [103, "ljcormier@gmail.com", "Porky", "porky", 0, 1, "LeeC", "E", "BLuc", 0],
                [92, "pjlefeb@gmail.com", "pjlefeb", "flavanh", 0, 1, "Paul L", "Ben", "Ben", 0],
                [95, "pennamar@comcast.net", "Porro", "ceilidh", 0, 1, "RayPen", "Ben", "RP", 0],
                [97, "justinverret@me.com", "PAEasy", "tresv5", 0, 1, "JV", "Ben", "DC", 0],
                [105, "tob2@comcast.net", "Maximus", "terry", 0, 1, "Terry", "E", "BLb", 0],
                [106, "cpaq32@yahoo.com", "Millyard Masons", "winner", 0, 1, "Calin", "E", "BPaq", 0],
                [107, "hmaster2@aol.com", "The Rock", "dixie", 0, 1, "R-Terry", "E", "BLb", 0],
                [109, "rfmbrookside@aol.com", "Homer", "homer", 0, 1, "H", "E", "DC", 0],
                [111, "dbl.barry@comcast.net", "DBL315", "lauren5858", 0, 1, "BB", "NPNPNP", "BB", 0],
                [133, "gm_fletcher@hotmail.com", "Fletch", "skiing5", 0, 1, "Fletch", "E", "AS", 0],
                [116, "jpboyle25@yahoo.com", "Pete25", "boyle", 0, 1, "JPBoyle", "E", "Kn", 0],
                [119, "markapomerleau@gmail.com", "sacked", "mark3030", 0, 1, "Mark P", "E", "DanB", 0],
                [124, "nstatires@gmail.com", "Nick Stat", "Njs=122", 0, 1, "Nick", "E", "AS", 0],
                [125, "william.statires@gmail.com", "B Stats", "Bjs-4242", 0, 1, "Billy St", "E", "AS", 0],
                [126, "Micablanchette@gmail.com", "Neon Deion", "soccer22", 0, 1, "Mica", "E", "Kn", 0],
                [127, "doucetn3@gmail.com", "Little Dent", "nick3", 0, 1, "Nicky", "E", "MD", 0],
                [128, "kstatires@gmail.com", "kstat", "kstat123", 0, 1, "Kristen", "E", "AS", 0],
                [130, "shawn@fsrp.net", "Bueller", "monty4121", 0, 1, "ShawnM", "E", "BLab", 0],
                [131, "charlielikerman@yahoo.com", "Wiley Coyote", "charlie", 0, 1, "Charlie", "Ben", "BLab", 0],
                [134, "ballirostyle@yahoo.com", "Style", "zxc9040", 0, 1, "Tia", "E", "BLab", 0],
                [206, "Paul17nh@yahoo.com", "Dolomites", "Dolomites1", 0, 1, "Paul", "E", "Buddy", 0],
                [138, "joshuabernier85@gmail.com", "Raging Turf Tip", "brayden1", 0, 1, "JBernier", "E", "DanB", 0],
                [140, "bdoyle978@hotmail.com", "vargas", "newman11", 0, 1, "BDoyle", "Ben", "BD", 0],
                [142, "Scott_stclair@yahoo.com", "Hugh Jarse", "RhSs2299", 0, 1, "ScottSC", "Ben", "SS", 0],
                [143, "jeffnkimwhite@gmail.com", "3Whitesand1Moore", "6209Jeff", 0, 1, "K and J", "E", "KW", 0],
                [146, "jharris@helixaz.com", "jeffharris", "Bogey4321", 0, 1, "JHarris", "Ben", "JH", 0],
                [147, "mixmastermerch@hotmail.com", "Xecutioners", "hoochie", 0, 1, "J Hayes", "E", "MD", 0],
                [173, "Tdot5498@yahoo.com", "TommyD", "moss81", 0, 1, "Tm D", "E", "Kn", 0],
                [160, "ajscalingi@gmail.com", "Scuge", "Tombrady12", 0, 1, "???", "NPNPNP", "MD", 0],
                [157, "jimsims12@gmail.com", "Team JSims", "celtics9436", 0, 1, "JSims", "E", "AS", 0],
                [158, "rich.webber@hotmail.com", "Caveman", "323334", 0, 1, "RichW", "E", "MD", 0],
                [159, "rdiburro@yahoo.com", "G-Rod", "reynolds", 0, 1, "ND Fr", "E", "MD", 0],
                [163, "Brownadr@bc.edu", "Ryan Brown", "trotnixon", 0, 1, "RyanB", "E", "AS", 0],
                [164, "mthomas1169@yahoo.com", "GFY11", "Tooth", 0, 1, "MattTh", "E", "KTh", 0],
                [165, "danboyle51@yahoo.com", "ainge", "dan51", 0, 1, "DanB", "E", "Kn", 0],
                [166, "ejskillings@gmail.com", "BIG SKILLIE", "749ukhsv49", 0, 1, "Eric Sk", "E", "MF", 0],
                [167, "sbloughlin@gmail.com", "THE  RECYCLER", "and14444", 0, 1, "", "E", "BHam", 0],
                [168, "sgaryn@yahoo.com", "stephen garyn", "nanapoppy", 0, 1, "Ryan""sGr", "E", "AS", 0],
                [170, "jpnkr10@gmail.com", "Pinkys Money Picks", "jan1987", 0, 1, "J Pink", "E", "DanB", 0],
                [199, "estys1212@gmail.com", "stys1212", "falcons20", 0, 1, "Estys", "E", "WilSt", 0],
                [174, "nicksims34@gmail.com", "South Paw", "Redsox24", 0, 1, "N Sims", "E", "A St", 0],
                [175, "mathewhorlacher@gmail.com", "HORslacker", "Thehor44", 0, 1, "Matt H", "Ben", "MH", 0],
                [176, "Rluther8@yahoo.com", "Marines", "bodhi8", 0, 1, "RLuther", "E", "AStat", 0],
                [177, "apdental@comcast.net", "Green & Gold", "packers", 0, 1, "APD", "E", "BLuc", 0],
                [178, "krv154@hotmail.com", "Runnin Jalapeno", "javPRVkrv", 0, 1, "", "NPNPNP", "MF", 0],
                [179, "flemingbd@yahoo.com", "Flem's Famous Jinx", "dakota", 0, 1, "BFlem", "Ben", "BF", 0],
                [180, "brianpfitzgerald@gmail.com", "The Gun Show", "sunkist", 0, 1, "BFitz", "E", "DC", 0],
                [181, "kmeis919@gmail.com", "KM919", "kevin", 0, 1, "KevMeisel", "E", "IW", 0],
                [182, "Mcdonoughj21@yahoo.com", "Jose Bananez", "clippers17", 0, 1, "McD", "E", "Kn", 0],
                [183, "flynnah14@gmail.com", "InLikeFlynn", "Patrick-14", 0, 1, "Flynr", "E", "Kn", 0],
                [184, "webbco@comcast.net", "webbco", "vicki", 0, 1, "Vicki", "Ben", "BDoyle", 0],
                [195, "jjgbfan17@gmail.com", "JJ St.Pierre", "hota17", 0, 1, "JJ", "E", "MD", 0],
                [193, "M.fitzpatrick2010@comcast.net", "Macker", "Nala33", 0, 1, "M Fitz", "E", "MF", 0],
                [194, "ecollins@gatewayscs.org", "silver rush", "peanut", 0, 1, "EdColl", "E", "BLuc", 0],
                [196, "rbloom1013@gmail.com", "Coney Island", "pigpicksv", 0, 1, "RBloom", "Ben", "JHarris", 0],
                [197, "riordanfitzz@gmail.com", "LRFITZ", "etarepsed", 0, 1, "Liam", "E", "MF", 0],
                [198, "Kaguh1@Unh.newhaven.edu", "Noooobody", "kings5", 0, 1, "ND Fr", "E", "MD", 0],
                [200, "Leach24@gmail.com", "MarkBrunellisBroke", "kennedy", 0, 1, "RLeach", "Ben", "RLeach", 0],
                [201, "esims17@gmail.com", "Team Eliz", "123jacoby", 0, 1, "Eliz", "E", "WilSt", 0],
                [202, "dstravis1717@gmail.com", "Trav1717", "dstravis", 0, 1, "DTrav", "Ben", "M Tr", 0],
                [203, "steveg7753@gmail.com", "steveg7753", "Samantha1", 0, 1, "SteveG", "Ben", "Ben", 0],
                [204, "mdoucet56@gmail.com", "Jaundiced Eye", "midget", 0, 1, "MD", "E", "MD", 0],
                [205, "toddburley26@gmail.com", "tmb4play", "5tb072501", 0, 1, "TB", "E", "JWh", 0]]

    for user in user_list:
        new_user = User(
            user_email = user[1],
            user_team_name = user[2],
            user_password = user[3],
            user_paid = user[4],
            user_n = user[6],
            user_af1 = user[7],
            user_af2 = user[8]
        )
        new_user.save()
