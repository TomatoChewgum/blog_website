var data = [];

var dataStr = "1.DeathNote;Japanese Cartoon#\
                2.FateUBW;Japanese Cartoon#\
3.FateZero;Japanese Cartoon#\
4.GoneGirl;American Movie#"

var d = dataStr.split("#");
for (var i = 0; i < d.length; i++) {
    var c = d[i].split(";");
    data.push({
        img: c[0] + ".jpg",
        caption: c[0].split(".")[1],
        desc: c[1]
    });
}

// data[0].img = "2.FateUBW.jpg"