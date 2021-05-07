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
            if(data['message'] == "Success"){
                window.location.href = next;
            }
            else{
                $("#login_error").html("Invalid login data. Try again");
            }
        }
    });
}


function add_task(endpoint){
    title = document.getElementById("title").value;
    date = document.getElementById("date").value;
    priority = document.getElementById("priority").value;
    goal = document.getElementById("goal").value;
    status = document.getElementById("status").checked;
    csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $("#date_error").html("");
    $.ajax({
        type:"POST",
        url: endpoint,
        data:{
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'title': title,
            'date': date,
            'priority': priority,
            'goal': goal,
            'status': status
        },
        success : function(response){
            if(response == "ok"){
                $('#add_task').modal('hide');
                location.reload();
            }
            else if(response == "date error"){
                $("#date_error").html("Wrong date format");
            }
        }
    });
}


