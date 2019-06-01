import config from 'config';

export const prepareTable = table => ({
    title: `${table.pageTitle} - ${table.tableTitle}`,
    tableSource: `${config.get('baseurl')}page/${table.pageID}`,
    nextTable: `${config.get('baseurl')}table/next`,
    saveTable: `${config.get('baseurl')}table/${table._id}`,
    skipTable: `${config.get('baseurl')}table/${table._id}/skip`,
    html: table.taggedHtml,
    initialState: {
        annotations: table.annotations
    }
});
