var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function submitForm(id){
    console.log("kinda submitted the form");
    var d_ok = $("input[name='ok']").val();
    var d_ok_stare = $("input[name='ok_stare']").val();
    var d_upr = $("input[name='upr']").val();
    var d_upr_stare = $("input[name='upr_stare']").val();
    console.log("sending OK:  " + d_ok);
    console.log("sending UPR: " + d_upr);
    console.log("old OK:      " + d_ok_stare);
    console.log("old UPR:     " + d_upr_stare);
    $.ajax({
        url : 'obwod/' + id + '/',
        type: "POST",
        data: {
            ok: d_ok,
            ok_stare: d_ok_stare,
            upr: d_upr,
            upr_stare: d_upr_stare
        },
        success: function(json){
            console.log("success");
            if(json.status != "OK" && json.status != "DATA_CHANGED_OK" && json.status != "DATA_CHANGED_UPR"){
                $("#ok" + id).html(d_ok_stare);
                $("#upr" + id).html(d_upr_stare);
            }

            if(json.status == "OK") {
                console.log("sukces bardzo");
                $("#ok" + id).html(json.ok);
                $("#upr" + id).html(json.upr);
                alert("Zapisano dane");
            }else if(json.status == "OBWOD_NOT_FOUND"){
                console.log("obwod 404 :<");
                alert("Nie ma takiego obwodu");
            }else if(json.status == "WRONG_DATA"){
                console.log("bad data");
                alert("Błędne dane");
            }else if(json.status == "INCOMPLETE_DATA"){
                console.log("incomplete data");
                alert("Niekompletne dane");
            }else if(json.status == "NEGATIVE_NUMBERS"){
                console.log("negative numbers");
                alert("Nie można wprowadzać ujemnych liczb");
            }else if(json.status == "DATA_CHANGED") {
                console.log("data change");
                getDataCancel(id);
                alert("Dane zmieniły się od ostatniego zapisu. Zapisujesz " + json.new + ", a ktoś inny zapisał " + json.original);
            }
        },
        error: function(xhr, errmsg){
            console.log("error");
            console.log(xhr.status + ": " + xhr.responseText + "\n" + errmsg);
            alert("An error has happened to happen.")
        }
    });
}


function getDataEdit(id){
    console.log("Gettin' data");
    $.ajax({
        url : 'obwod/' + id + '/',
        type: "GET",
        success: function(json){
            console.log("Got data: " + json.ok + " , " + json.upr);
            $("#ok" + id).replaceWith('<td id="ok' + id + '"><input type="hidden" name="ok_stare" value="' + json.ok + '" form="form' + id + '"><input type="text" name="ok" value="' + json.ok + '" form="form' + id + '"></td>');
            $("#upr" + id).replaceWith('<td id="upr' + id + '"><input type="hidden" name="upr_stare" value="' + json.upr + '" form="form' + id + '"><input type="text" name="upr" value="' + json.upr + '" form="form' + id + '"></td>');
        }
    })
}


function getDataCancel(id){
    console.log("Gettin' data");
    $.ajax({
        url : 'obwod/' + id + '/',
        type: "GET",
        success: function(json){
            console.log("Got data: " + json.ok + " , " + json.upr);
            $("#ok" + id).html(json.ok);
            $("#upr" + id).html(json.upr);}
    })
}


function zmiana(id) {
    console.log("editButton" + id);
    var subB = $("#submitButton" + id);
    var canB = $("#cancelButton" + id);
    var ediB = $("#editButton" + id);
    $(document).ready(subB.hide());
    $(document).ready(canB.hide());
    $(document).ready($("#form" + id).on('submit', function(event){
        event.preventDefault();
        submitForm(id);
    }));
    $(document).ready(ediB.click(function () {
        console.log("klik " + id);
        getDataEdit(id);
        ediB.hide();
        subB.show();
        canB.show();
        return false;
    }));
    $(document).ready(subB.click(function () {
        console.log("klik zapisz");
        $("#form" + id).submit();
        ediB.show();
        subB.hide();
        canB.hide();
        return false;
    }));
    $(document).ready(canB.click(function () {
        console.log("klik anuluj");
        getDataCancel(id);
        ediB.show();
        subB.hide();
        canB.hide();
        return false;
    }));
}