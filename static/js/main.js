
  const datetimme = setInterval(() =>{
    let date = new Date();
      $("#header_date").text( date.toLocaleDateString() );
      $("#header_time").text( date.toLocaleTimeString() );

  }, 1000);

const ShowData = (id)=>{
    $.ajax({
        url:`/student/${id}/`,
        method: 'POST',
        success: function(data){
            if(data.status =="success"){
                let st = data.data;
                $("#table_st_id").text(st.id)
                $("#table_name").text(st.name)
                $("#table_gender").text(st.gender)
                $("#table_class").text(st.class),
                $("#table_guardian").text(st.guardian),
                $("#table_phone").text(st.phone),
                $("#table_activity").text(st.activities)
                $("#my_modal_2").attr('open','true');
                if(st.image != ''){
                    $("#table_image").attr('src',st.image);

                    $("#table_image").removeClass('hidden');
                    $("#table_alternate_image").addClass('hidden');
                }else{
                    $("#table_image").addClass('hidden');
                    $("#table_alternate_image").removeClass('hidden');
                }
                
                $("#table_delete").attr('href',`/student/delete/${st.id}/`);
                $("#table_print").attr('href',`/student/print/${st.id}/`);
                $("#table_update").attr('href',`/student/update/${st.id}/`);
                
            }
            else{
                alert("Failed to load student data!");
            }
        },
    });
    // alert(id);
}


function debounce(func, timeout = 750){
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
  }

$(document).ready(function() {


    if( $("#id_school_name").val() == "NA"){
        console.log($("#id_school_name").val());
        $("#other_school_name_container").removeClass("hidden");
    }

    $("#id_image").on("change", function(e){
        // console.log(e.target.result);
        $("#gender_icon_male").addClass("hidden");
        $("#gender_icon_female").addClass("hidden");
        $("#aaa").attr("src", URL.createObjectURL(e.target.files[0])).removeClass("hidden");
    }); 



    var selected_activity ={
        act1:  $("#id_activity1").val() ? $("#id_activity1").val() : 0,
        act2: $("#id_activity2").val() ? $("#id_activity2").val() : 0,
        act3: $("#id_activity3").val() ? $("#id_activity3").val() : 0,
        time1: $("#id_time1").val() ? $("#id_time1").val() : 0,
        time2: $("#id_time2").val() ? $("#id_time2").val() : 0,
        time3: $("#id_time3").val() ? $("#id_time3").val() : 0,
    };

    $("#id_activity1").on("change", debounce(function(e){
        let val = $(e.target).val().toString();
        if(val == selected_activity.act2 || val == selected_activity.act3){
            alert("Already selected");
            $(e.target).prop('selectedIndex',0);
            selected_activity.act1 = 0;
            $(e.target).focus();
        }else{
            selected_activity.act1 = val;
        }

    }));

    $("#id_activity2").on("change", debounce(function(e){
        let val = $(e.target).val().toString();
        if(val == selected_activity.act1 || val == selected_activity.act3){
            alert("Already selected");
            $(e.target).prop('selectedIndex',0);
            $(e.target).focus();
            selected_activity.act2 = 0;

        }else{
            selected_activity.act2 = val;
        }
    }));

    $("#id_activity3").on("change", debounce(function(e){

        let val = $(e.target).val().toString();
        if(val == selected_activity.act1 || val == selected_activity.act2){
            alert("Already selected");
            $(e.target).prop('selectedIndex',0);
            selected_activity.act3 = 0;
            $(e.target).focus();
        }else{
            selected_activity.act3 = val;
        }

    }));


    $("#id_time1").on("change", debounce(function(e){

        let val = $(e.target).val().toString();
        if(val == selected_activity.time2 || val == selected_activity.time3){
            alert("Already selected");
            $(e.target).prop('selectedIndex',0);
            selected_activity.time1 = 0;
            $(e.target).focus();
        }else{
            selected_activity.time1 = val;
        }
    }));

    
    $("#id_time2").on("change", debounce(function(e){
        let val = $(e.target).val().toString();
        if(val == selected_activity.time1 || val == selected_activity.time3){
            alert("Already selected");
            $(e.target).prop('selectedIndex',0);
            selected_activity.time2 = 0;
            $(e.target).focus();
        }else{
            selected_activity.time2 = val;
        }
    }));

    $("#id_time3").on("change", debounce(function(e){
        let val = $(e.target).val().toString();
        if(val == selected_activity.time1 || val == selected_activity.time2){
            alert("Already selected");
            $(e.target).prop('selectedIndex',0);
            selected_activity.time3 = 0;
            $(e.target).focus();
        }else{
            selected_activity.time3 = val;
        }
    }));

    $("#id_gender").on("change", function(e) {
        let value = $(e.target).val();
        if(value == "F"){
            $("#gender_icon_male").addClass("hidden");
            $("#gender_icon_female").removeClass("hidden");
        }
        else if(value=="M"){
            $("#gender_icon_male").removeClass("hidden");
            $("#gender_icon_female").addClass("hidden");

        }else{
            $("#gender_icon_male").removeClass("hidden");
            $("#gender_icon_female").addClass("hidden");
        }
    });

    $("#id_school_name").on("change", function(e) {
        let value = $(e.target).val();
        if(value == "NA")
        $("#other_school_name_container").removeClass("hidden");
        else
        $("#other_school_name_container").addClass("hidden");

    });
});