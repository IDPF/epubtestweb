
function DT() { }

DT.prototype.initialize = function(options) {
    this.fixedHeader = options.fixedHeader !== undefined ? Boolean(options.fixedHeader) : true;
    this.fixedCol = options.fixedColumn !== undefined ? Boolean(options.fixedColumn) : false;
    this.searchable = options.searchable !== undefined ? Boolean(options.searchable) : true;
    this.setDefaultSort = options.setDefaultSort !== undefined ? Boolean(options.setDefaultSort) : true;
    this.changeDefaultSort = options.changeDefaultSort !== undefined ? Boolean(options.changeDefaultSort) : true;
    this.srchLabel = (options.srchLabel == undefined || options.srchLabel == null || options.srchLabel == '') ? 'Find Reading System(s) ' : options.srchLabel;
    this.srchPlaceholder = (options.srchPlaceholder == undefined || options.srchLabel == null || options.srchPlaceholder == '') ? 'Enter a name or operating system' : options.srchPlaceholder;
    this.isMobile = window.matchMedia("only screen and (max-device-width: 760px)").matches;
    this.tableType = options.tableType;
    
    this.enhance();
}

DT.prototype.enhance = function() {
    var tables = document.getElementsByTagName('table');
    
    // add table ids to a non-dynamic list (datatables will grow the # of tables as they're made dynamic)
    var IDs = [];
    for (var i = 0; i < tables.length; i++) {
        var thisID = tables[i].id;
        if (typeof thisID !== undefined && thisID !== null && thisID != '') {
            IDs.push(thisID);
        }
    }
    
    for (var j = 0; j < IDs.length; j++) {
        this.makeDynamic(IDs[j]);
        if (this.changeDefaultSort) {
           this.changeSort(IDs[j]);
        }
    }
    
    // set the table view linking + cookie
    this.setUserView();
}

DT.prototype.makeDynamic = function(tblID) {

    if ( $.fn.DataTable.isDataTable('#'+tblID) ) {
        $('#'+tblID).DataTable().destroy();
    }
    
    var table;
    
    if (this.fixedCol) {
        table = $('#'+tblID).DataTable({
            "paging": false,
            "info": false,
            "searching": this.searchable,
            "stateSave": true,
            "autoWidth": false,
            "scrollY": '50vh',
            "scrollX": true,
            "scrollCollapse": false,
            "fixedColumns": {
                "leftColumns": 1
            },
            "oLanguage": {
                "sSearch": this.srchLabel,
                "sSearchPlaceholder": this.srchPlaceholder
            }
        });
    }
    else {
        table = $('#'+tblID).DataTable({
            "paging": false,
            "info": false,
            "searching": this.searchable,
            "stateSave": true,
            "autoWidth": false,
            "aaSorting": this.setDefaultSort ? [0,'asc'] : [],
            "oLanguage": {
                "sSearch": this.srchLabel,
                "sSearchPlaceholder": this.srchPlaceholder
            }
        });
    }
    
    if (this.fixedHeader) {
        new $.fn.dataTable.FixedHeader( table, {
            // options
        });
    }
}

DT.prototype.changeSort = function(tblID) {
    var oTable = $('#'+tblID).dataTable();
    var oSettings = oTable.fnSettings();
    var iColumns = oSettings.aoColumns.length - 1;
    
    for (var i = 0; i <= iColumns; i++) {
        var colName = oSettings.aoColumns[i].sTitle.toLowerCase();
        if (colName != '#' && colName != 'name' && colName != 'at' && colName != 'description') {
            oSettings.aoColumns[i].asSorting = ['desc','asc'];
        }
    }
}

DT.prototype.setUserView = function() {    
    if (this.tableType == 'col') {
        Cookies.set('tblType', 'col', { expires: 365 });
        this.setTableViewLinks('col','hd');
    }
    else {
        Cookies.set('tblType', 'hd', { expires: 365 });
        this.setTableViewLinks('hd','col');
    }
}

DT.prototype.setTableViewLinks = function(active, inactive) {
    $('#'+active).unbind('click');
    $('#'+active).addClass('inactiveLink');
    $('#'+inactive).bind('click');
    $('#'+inactive).removeClass('inactiveLink');
}

DT.prototype.getTableType = function() {
    var tblType = Cookies.get('tblType'); ;
    
    if (typeof(tblType) == 'undefined' || tblType == null || tblType == '') {
        Cookies.set('tblType', 'hd', { expires: 365 });
    }
    
    return tblType;
}
