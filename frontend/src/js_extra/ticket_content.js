
import {term_lookup} from '../js_extra/utils.js';


function htmlEncode (str){
    return str.replace(/[\u00A0-\u9999<>&]/gim, function(i) {
       return '&#'+i.charCodeAt(0)+';';
    });
}


function print_requested_field(field){
    return field;
 }

function requested_fields_html(init_data,requested_fields){
    return "<dt>Requested fields:</dt><dd><ul style='padding-left:0;'><li>"
            + requested_fields.map(item => {return print_requested_field(item);}).join('</li><li>')
            + "</li></ul></dd>";
}

function progs_adm_html(init_data,progs_selected){
    var progs_print = "<dt>Programs:</dt><dd><ul style='padding-left:0;'>";
    var i;   
    if ("first_year" in progs_selected){
       progs_print = progs_print + "<li>First year:<ul>";
       const first_year=progs_selected.first_year;
       for (const faculty in first_year){
          progs_print = progs_print + "<li>" + faculty + ":<ul>";
          const progs = first_year[faculty];
          for (i=0;i<progs.length;i++){
             progs_print = progs_print + "<li>" + init_data.faculties[faculty][progs[i]] + "</li>"
          }                     
          progs_print = progs_print + "</ul></li>";
       }
       progs_print = progs_print + "</ul></li>";
    }
    //other_plans_progs
    if ("upper_year" in progs_selected){
       progs_print = progs_print + "<li>Upper year:<ul>";
       const progplans = progs_selected.upper_year;
       for (i=0; i< progplans.length; i++){
          progs_print = progs_print + "<li>" + progplans[i] + "</li>";
       }

       progs_print = progs_print + "</ul></li>";
    }
    progs_print = progs_print + "</ul></dd>";
    return progs_print;
}

function progs_student_html(init_data,progs_selected){
    var progs_print = "<dt>Programs and Plans:</dt><dd><ul style='padding-left:0;'>";
    var i;
    //common progs
    if ("common_progs" in progs_selected){
        progs_print = progs_print + "<li>Commonly requested programs:<ul>";
        const common_progs=progs_selected.common_progs;
        for (const faculty in common_progs){
            progs_print = progs_print + "<li>" + faculty + ":<ul>";
            const progs = common_progs[faculty];
            for (const prog in progs ){
                progs_print = progs_print + "<li>" + init_data.faculties_student[faculty].progs[prog].longhand;
                if (progs[prog]===true){
                    progs_print = progs_print + ": <i>All</i>";
                }else if (progs[prog].length > 0){
                    progs_print = progs_print + ":<ul>"
                    for(i=0;i<progs[prog].length;i++){
                        progs_print = progs_print + "<li>" + progs[prog][i] + "</li>";
                    }
                    progs_print = progs_print + "</ul>"
                }

                progs_print = progs_print + "</li>"
            }
                     
            progs_print = progs_print + "</ul></li>";
        }

        progs_print = progs_print + "</ul></li>";
    }
    //other_plans_progs
    if ("other_plans_progs" in progs_selected){
        progs_print = progs_print + "<li>Other programs and plans:<ul>";
        const progplans = progs_selected.other_plans_progs;
        for (i=0; i< progplans.length; i++){
            progs_print = progs_print + "<li>" + progplans[i] + "</li>";
        }
        progs_print = progs_print + "</ul></li>";
    }

    progs_print = progs_print + "</ul></dd>";
    return progs_print;
}

function list_choices_html(init_data,list_choices){
    var list_print = "";
    var item;
    for (item in list_choices){
        const choices = list_choices[item];
        const list_def = init_data.data_lists[item];
        const header = list_def.heading;
        list_print = list_print + "<dt>" + header + ":</dt><dd><ul style='padding-left:0;'><li>"
                                + choices.map(item => list_def.items[item]).join('</li><li>')
                                + "</li></ul></dd>"

    }
    return list_print;
}

function terms_html(form_type,terms_selected){
    var terms_print;
    var term_label;
    term_label = form_type == "admissions"?"Admit terms":"Terms";
    terms_print = "<dt>" + term_label + ":</dt>";
    terms_print = terms_print + "<dd><ul style='padding-left:0;'><li>";
    terms_print = terms_print + terms_selected.map (ps_term => {
                        return term_lookup(ps_term) + " (" + ps_term + ")";
                    }).join("</li><li>");
    terms_print = terms_print + "</li></ul></dd>";
    return terms_print;
}


function requested_before_html(content_data){
    var result="<dt>Requested Before:</dt><dd>No</dd>";
    if ("prev_report_info" in content_data){

        result = "<dt>Requested Before:</dt><dd>Yes</dd>"
                        + "<dt>Previous Report Info:</dt><dd>"
                        + htmlEncode(content_data.prev_report_info)
                        + "</dd>"
    }
    return result;
}

function source_choice_html(init_data,source_choice){
    var report_txt;
    if (source_choice.rpt_source_type=="standard"){
        report_txt = init_data.data_support_choices[source_choice.source_key];
    }else{
        report_txt = source_choice.description; 
    }
    var result;
    result = "<dt>Report source:</dt><dd>"
                + report_txt + "</dd>";
    return result;
}



function create_html(init_data,form_type,content_data){
    var result = "<dl>" +
                ("request_type" in content_data?("<dt>Request Type:</dt>" + "<dd>" + init_data.request_types[form_type] +"</dd>"):"") +
                ("subject" in content_data && form_type != "rptsupport"?("<dt>Report Title:</dt>" + "<dd>" + htmlEncode(content_data.subject) + "</dd>"):"") +
                ("requestor_name" in content_data?("<dt>Requestor Name:</dt>" + "<dd>" + htmlEncode(content_data.requestor_name) + "</dd>"):"") +
                ("requestor_dept" in content_data?("<dt>Requestor Dept:</dt>" + "<dd>" + htmlEncode(content_data.requestor_dept) + "</dd>"):"") +
                ("dueDate" in content_data?("<dt>Due date:</dt><dd>" + content_data.dueDate + "</dd>"):"") +
                ("requestor_position" in content_data?("<dt>Requestor Position:</dt>" + "<dd>" + htmlEncode(content_data.requestor_position) + "</dd>"):"") +
                (form_type!="rptsupport"?requested_before_html(content_data):"") +
                ("report_purpose" in content_data?"<dt>Report Purpose:</dt><dd>" + htmlEncode(content_data.report_purpose) + "</dd>":"") +
                ("source_choice" in content_data?source_choice_html(init_data,content_data.source_choice):"") +
                ("support_request_descr" in content_data?"<dt>Problem Description:</dt><dd>" + htmlEncode(content_data.support_request_descr) + "</dd>":"");
    if ("terms" in content_data){
        result = result + terms_html(form_type,content_data.terms);
    }

    if ("progs" in content_data){
        if (form_type == "admissions"){
            result = result + progs_adm_html(init_data,content_data.progs);
        }else{
            result = result + progs_student_html(init_data,content_data.progs); 
        }
    }
    if ("list_choices" in content_data){
        result = result + list_choices_html(init_data,content_data.list_choices);
    }
    if ("extra_details" in content_data){
        result = result + "<dt>Extra Details:</dt><dd>" + htmlEncode(content_data.extra_details) + "</dd>"
    }

    if("requested_fields" in content_data){
        result = result + requested_fields_html(init_data,content_data.requested_fields);
    }

    result = result + "</dl>"
    return result;
}

export { create_html }