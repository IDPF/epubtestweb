
function DT() { }

DT.prototype.initialize = function(options) {
    this.searchable = options.searchable !== undefined ? Boolean(options.searchable) : true;
    this.setDefaultSort = options.setDefaultSort !== undefined ? Boolean(options.setDefaultSort) : true;
    this.changeDefaultSort = options.changeDefaultSort !== undefined ? Boolean(options.changeDefaultSort) : true;
    this.srchLabel = (options.srchLabel == undefined || options.srchLabel == null || options.srchLabel == '') ? 'Find in table ' : options.srchLabel;
    this.srchPlaceholder = (options.srchPlaceholder == undefined || options.srchLabel == null || options.srchPlaceholder == '') ? 'Enter a name or operating system' : options.srchPlaceholder;
    
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

    var tblRef = '#'+tblID;
    
    if ( $.fn.DataTable.isDataTable('#'+tblID) ) {
        $(tblRef).DataTable().destroy();
    }
    
    if (this.tableType == 'basic') {
        // destroy leaves thead after tbody if switching from fixed header so hack to reverse
        $(tblRef+' > thead').after($(tblRef+' > tbody'));
        $(tblRef).DataTable({
                "paging": false,
                "info": false,
                "searching": this.searchable,
                "aaSorting": this.setDefaultSort ? [0,'asc'] : [],
                "oLanguage": {
                    "sSearch": this.srchLabel,
                    "sSearchPlaceholder": this.srchPlaceholder
                }
            });
    }
    
    else {
        var table;
        
        if (this.fixedCol) {
            table = $(tblRef).DataTable({
                "paging": false,
                "info": false,
                "searching": this.searchable,
                "stateSave": true,
                "autoWidth": false,
                "aaSorting": this.setDefaultSort ? [0,'asc'] : [],
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
            table = $(tblRef).DataTable({
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
            new $.fn.dataTable.FixedHeader( table, { });
        }
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
        this.setTableViewLinks('col','hd','basic');
    }
    else if (this.tableType == 'hd') {
        Cookies.set('tblType', 'hd', { expires: 365 });
        this.setTableViewLinks('hd','col','basic');
    }
    else {
        Cookies.set('tblType', 'basic', { expires: 365 });
        this.setTableViewLinks('basic','col','hd');
    }
}

DT.prototype.setTableViewLinks = function(active, inactive, inactive2) {
    $('#'+active).unbind('click');
    $('#'+active).addClass('inactiveLink');
    $('#'+inactive).bind('click');
    $('#'+inactive).removeClass('inactiveLink');
    $('#'+inactive2).bind('click');
    $('#'+inactive2).removeClass('inactiveLink');
}

DT.prototype.setTableType = function(tblType) {
    
    if (typeof(tblType) == 'undefined' || tblType == null || tblType == '') {
        tblType = Cookies.get('tblType');
        if (typeof(tblType) == 'undefined' || tblType == null || tblType == '') {
            Cookies.set('tblType', 'basic', { expires: 365 });
            tblType = 'basic';
        }
    }
    
    this.tableType = tblType;
    this.fixedHeader = !(tblType == 'col');
    this.fixedCol = (tblType == 'col');
}
