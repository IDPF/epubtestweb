
function DT(options) {
    this.fixedHeader = options.fixedHeader !== undefined ? Boolean(options.fixedHeader) : true;
    this.fixedCol = options.fixedColumn !== undefined ? Boolean(options.fixedColumn) : false;
    this.searchable = options.searchable !== undefined ? Boolean(options.searchable) : true;
    this.setDefaultSort = options.setDefaultSort !== undefined ? Boolean(options.setDefaultSort) : true;
    this.changeDefaultSort = options.changeDefaultSort !== undefined ? Boolean(options.changeDefaultSort) : true;
    this.srchLabel = (options.srchLabel == undefined || options.srchLabel == null || options.srchLabel == '') ? 'Find Reading System(s) ' : options.srchLabel;
    this.srchPlaceholder = (options.srchPlaceholder == undefined || options.srchLabel == null || options.srchPlaceholder == '') ? 'Enter a name or operating system' : options.srchPlaceholder;
    this.isMobile = window.matchMedia("max-width: 760px").matches;
}

DT.prototype.initTables = function() {
    var tables = document.getElementsByTagName('table');
    
    // add table ids to a non-dynamic list (datatables will grow the # of tables as they're made dynamic)
    var ids = new Array(tables.length-1);
    for (var i = 0; i < tables.length; i++) {
        ids[i] = tables[i].id;
    }
    
    for (var j = 0; j < ids.length; j++) {
        this.makeDynamic(ids[j]);
        if (this.changeDefaultSort) {
           this.changeSort(ids[j]);
        }
    }
}

DT.prototype.makeDynamic = function(tblID) {

    var table;
    
    if (this.isMobile) {
        $('#'+tblID).DataTable({
            "paging": false,
            "info": false,
            "stateSave": true,
            "responsive": {
                "details": {
                    "display": $.fn.dataTable.Responsive.display.childRowImmediate,
                    "type": ''
                }
            },
            "oLanguage": {
                "sSearch": this.srchLabel,
                "sSearchPlaceholder": this.srchPlaceholder
            }
        });
    }
    else {
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
    }
    
    if (!this.isMobile && this.fixedHeader) {
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
 