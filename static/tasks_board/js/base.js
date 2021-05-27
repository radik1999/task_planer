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

// $(function(){
//   $('.modal-content').keypress(function(e){
//     if(e.which === 13) {
//       $(".add_task_bth").click();
//     }
//   })
// })
function add_task(endpoint, modal_id){

    title = document.querySelector(modal_id + " .title").value;
    date = document.querySelector(modal_id + " .date").value;
    priority = document.querySelector(modal_id + " .priority").value;
    goal = document.querySelector(modal_id + " .goal").value;
    main_task = document.querySelector(modal_id + " .main_task").value
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
            'main_task': main_task
        },
        success : function(response){
            if(response == "ok"){
                location.reload();
            }
            console.log(response)
            if(response === "date error"){
                $(modal_id + " #date_error").html("Wrong date format");
            }
            if(response === 'blank title'){
                $(modal_id + " #title_error").html("Title should not be blank");
            }
        }
    });
}

function add_goal(endpoint, modal_id){
    title = document.querySelector(modal_id + " .title").value;
    priority = document.querySelector(modal_id + " .priority").value;
    csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    $.ajax({
        type:"POST",
        url: endpoint,
        data:{
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'title': title,
            'priority': priority,
        },
        success : function(response){
            if(response == "ok"){
                location.reload();
            }
            if (response == 'blank title'){
                $("#title_error").html("Title should not be blank");
            }
        }
    });
}

function change_status(url){
    csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $.ajax({
        type:"POST",
        url: url,
        data: {
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        },
        success : function(response){
            if(response == "ok"){
                location.reload();
            }
        }
    })
}

window.addEventListener('load', add_active_class)


function add_active_class(element){
    let link = location.pathname
    let active_link = document.querySelector(".left-nav a[href='" + link + "']")
    if (link.includes('goal')){
        document.querySelector('#goals_nav').classList.add('show')
    }
    active_link.classList.add("active")
}

// function add_modal(element){
//     let html_code = element.getAttribute('about')
//     $('.statistic').prepend(html_code)
// }

function add_modal(modal_id){
    let mod = document.getElementById(modal_id);
    if (!mod){
        $.ajax({
        type:"GET",
        url: '/chart/' + modal_id,
        success : function(response){
            $('.statistic').prepend(response);
            mod = $('#' + modal_id);
            mod.modal('show');
        }
        })
    }
    else{
        mod = $('#' + modal_id);
        mod.modal('show');
    }


}

