var row_count=1
var row
var table_content="\n"
var favourite_json

var final_tour_table="final-tour-table"
var favourite_tour_table="favourite-tour-table"
//test
//adds user selected restaurants to final_tour_table
function addTour(){
        //html checkbox parent id  search result table .
        var e = event.target.parentNode.parentNode.id;
        var row_item=document.getElementById(e);
        //Reference the CheckBox in Table.
        var active_checkbox = row_item.getElementsByTagName("INPUT");
        //find target final food tour table table element
        var table=document.getElementById(final_tour_table);
        //check for active checkbox
        if (active_checkbox[0].checked) {
                //create row and set attributes to it
                var new_row=table.insertRow(row_count);
                //set id of actioned item as new table's row id
                new_row.setAttribute("id" ,e);
                new_row.setAttribute("draggable","True");
                new_row.setAttribute("ondragstart" ,"dragStart()");
                new_row.setAttribute("ondragover","dragTarget()");
                //insert cell and values from result table to finalized tour table
                insert_cell(new_row,0,row_item.cells[1].innerHTML)
                insert_cell(new_row,1,row_item.cells[2].innerHTML)
                insert_cell(new_row,2,row_item.cells[3].innerHTML)
                //radio_buttons[i].checked=false;
                row_count+=1
        }
        //delete action for unselected checkbox
        if (! active_checkbox[0].checked) {
                table.rows.namedItem(e).remove();//Remove row if unchecked
                row_count-=1;
        }
    }

//insert row into the table
function insert_row(tableobject,row_number,id){
    var row_id = tableobject.insertRow(row_number);
    row_id.setAttribute("id" ,id);
    return row_id;

}
//insert cell into the row and  assign data into cells
function insert_cell(rowObject,cell_number,cell_data){
    var cell_id = rowObject.insertCell(cell_number);
    cell_id.innerHTML = cell_data;
}

function remove_favourite(){
    row_key = event.target.parentNode.parentNode.id;
    //remove from html table
    document.getElementById(favourite_tour_table).rows.namedItem(row_key).remove();
    //remove from local storage
    localStorage.removeItem(row_key);

}
function existing_favourite(){
      for (l=0 ; l < localStorage.length ;l++){
        key=localStorage.key(l);
        if (key.match('FoodTour')){
          display_favourtie(document.getElementById(favourite_tour_table),key);
        }
      }

}

//display favourite list to user
function display_favourtie(favourite_table,localStorage_key){
    //adding row data
    favourite_row = insert_row(favourite_table,favourite_table.rows.length,localStorage_key);
    fav_data=" "
    //fetch localstorage data
    json_obj=JSON.parse(localStorage.getItem(localStorage_key));
    for(j=0;j<json_obj.length ;j++){
      fav_data += (j+1)+"."+"Restaurant "+ json_obj[j].name +" \t with "+json_obj[j].rating+" rating \t at "+json_obj[j].distance_in_miles+" distance. <br>" ;}
    insert_cell(favourite_row,0,'Favourite tour list');
    insert_cell(favourite_row,1,fav_data);
    insert_cell(favourite_row,2,"<button type='button' value='Remove' name='Remove' onclick=remove_favourite();> Remove </button>");

}

//Adds user selecetd  tour list to favourite and keep the data persistant in local storage
function add_favourite(submit_value){
        var parse_status=parse_htmltable(submit_value)
        if(parse_status){
            let localstorage_key = 'FoodTour_'+ ( Math.random() * 100);
             //parse html table
            console.log(favourite_json)
            localStorage.setItem(localstorage_key,favourite_json)
            //fetch recently added value into localStorage and render it to viewer
            //keys=localStorage.key(localStorage.length-1);
            //fetch table id and add new rows and display  each favourite item added
            var favourite_table=document.getElementById(favourite_tour_table);
            //call to display favourites
            display_favourtie(favourite_table,localstorage_key)
        }
}

function parse_htmltable(filetype){
      //fetch values from final tour table in html
      var rows=document.getElementById(final_tour_table).rows;

      if (rows.length > 1){
        for(i=1 ;i <rows.length ;i++){
          //table_content+=rows[0].cells[0].innerHTML; //first column name
          table_content+=rows[i].cells[0].innerHTML+"\t";
          //table_content+=rows[0].cells[1].innerHTML; //second column name
          table_content+=rows[i].cells[1].innerHTML+"\t";
        //  table_content+=rows[0].cells[2].innerHTML; //third column name
          table_content+=parseFloat(rows[i].cells[2].innerHTML)+"\n";
        }
        //console.log(table_content);
        $.ajax({
          //work on crsf token
          type:'get',
          url : 'convert_text_dataframe',
          async: false,
          data :{table_content:table_content , convert_to: filetype },
          success:function(response){
            //console.log(response)
            //saving item as json object user button value type is favourite
            if (filetype =="Fav"){
                favourite_json= response;

            }
            table_content = " ";
            filetype = " ";
            //return response;
          }
        })
        return true;
      }

  else{

    alert("You have made no selection .please add list to tour and try again");
    return false;
  }
}

//functions to handle drag and drop  events
function dragStart(){
    //hold reference for current dragged row
    row = event.target;
  }

//function to drag to hovered row in table
function dragTarget(){
      //prevent default positon in order to allow drop of element
      var e= event;
      e.preventDefault();
      //move element to selected drop target
        let children= Array.from(e.target.parentNode.parentNode.children);
        if (children.indexOf(e.target.parentNode)>children.indexOf(row)){
          e.target.parentNode.after(row);
        }
        else{
          e.target.parnetNode.before(row);
        }
    }
