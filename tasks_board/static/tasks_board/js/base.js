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
};

// $(function(){
//   $('.modal-content').keypress(function(e){
//     if(e.which === 13) {
//       $(".add_task_bth").click();
//     }
//   })
// })
function add_task(endpoint){
    title = document.getElementById("title").value;
    date = document.getElementById("date").value;
    priority = document.getElementById("priority").value;
    goal = document.getElementById("goal").value;
    status = document.getElementById("status").checked;
    main_task = document.getElementById('main_task').value
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
            'status': status,
            'main_task': main_task
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
};

function change_status(url){
    csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $.ajax({
        type:"POST",
        url: url,
        data: {
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        },
        success : function(response){
            if(response == "ok") {
                location.reload();
            }
        }
    });
};

