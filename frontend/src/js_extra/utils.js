

const base_year = "1901";
const base_strm = "1011";

function term_lookup(strm){
   const last_digit = strm.slice(-1);
   const base_year_int = parseInt(base_year);
   const base_strm_int = parseInt(base_strm);
   const season_lookup = {
      '1': 'Winter',
      '5': 'Summer',
      '9': 'Fall'
   }
   const season = season_lookup[last_digit];
   const strm_int = parseInt(strm);
   const year_delta = Math.floor((strm_int-base_strm_int)/10);
   const year = base_year_int + year_delta;
   return year.toString() + " " + season;
}


function get_current_term(){
    var today = new Date();
    var m = String(today.getMonth())
    var yyyy = today.getFullYear();
    const base_year_int = parseInt(base_year);
    const base_strm_int = parseInt(base_strm);
    var seasonOffset;
    if (m >=0 && m<= 3) {
        seasonOffset = 0;
    }else if(m >= 4 && m <=7){
        seasonOffset = 4;
    }else{
        seasonOffset = 8;
    }
    const year_delta = yyyy - base_year_int;
    const strm_int = (year_delta * 10) + base_strm_int + seasonOffset;
    return strm_int.toString();
}


function get_strm_bounds(current_term){
    const strm_int = parseInt(current_term);
    const begin = (strm_int - 20).toString();
    const end = (strm_int + 10).toString();
    return {
        begin: begin,
        end: end
    }
}


function strm_get_prev(strm){
    const last_digit = strm.slice(-1);
    const strm_int = parseInt(strm);
    const subtraction_lookup = {
      '1': 2,
      '5': 4,
      '9': 4
    }
    const subtraction = subtraction_lookup[last_digit];
    const prev_strm_int = strm_int - subtraction;
    return prev_strm_int.toString();
}





function is_busday(day,holidays){
    const daynum = day.getUTCDay();

    if (daynum==0 || daynum ==6) {
        return false;
    }else{
        var holiday;
        var holiday_date;
        for (holiday of holidays){
            holiday_date= new Date(holiday)
            //holiday as date object 12:00 UTC time
            if (day.getTime() ==holiday_date.getTime()){
                return false;
            }
        }

    }
    return true;
}


function n_busdays_hence(n,holidays){
    //This may have been a stupid choice but we are not interested in time zones.
    //Therefore we are doing everything in the UTC time zone.
    //THe theory being that UTC is as close to a time-zoneless time-zone as we
    //are going to get.
    var result = new Date(new Date().toDateString() + " 00:00:00 UTC");
    //result should be the present date but at 12 AM UTC....

    var bus_days = 0;
    while (bus_days < n ) {
        //business_day

        
        result.setUTCDate(result.getUTCDate() + 1);
        //The above line should advance the date by one day.

        if (is_busday(result,holidays)){
            bus_days=bus_days + 1
        }

    }
    console.log("n_busdays_hence"+result);
    return result.getTime();

}

function is_n_busdays_hence(input_day_str,n,holidays){
    const five_busdays_hence = n_busdays_hence(5,holidays);
    const input_date = new Date(input_day_str);
    // input_date is 12:00 AM on date, UTC time...
    const input_date_t = input_date.getTime()
    const time_diff = (input_date_t - five_busdays_hence);
    return time_diff >= 0;
}





export {term_lookup, get_strm_bounds, strm_get_prev, get_current_term, is_n_busdays_hence};