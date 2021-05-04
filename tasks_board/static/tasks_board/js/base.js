function login_user(endpoint, next){
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;
    csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $("#login_error").html("");
    $.ajax({
        type:"POST",
        url: endpoint,
        data:{
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'username':username,
            'password':password,
        },
        success : function(data){
            console.log(data);
            if(data['message'] == "Success"){
                window.location.href = next;
                // location.reload(next)
            }
            else{
                $("#login_error").html("Invalid login data. Try again");
            }
        }
    });
}