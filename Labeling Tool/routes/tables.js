import express from 'express';
import createError from 'http-errors';
import { connectToDB } from '../helpers/mongo';

const router = express.Router();

router.get('/next', (req, res) =>
    connectToDB()
        .then(({ client, tables }) =>
            tables
                .find({
                    annotation : {
                        $exists : false,
                    },
                    skipped: {
                        $ne: true
                    }
                })
                .limit(1)
                .next()
                .finally(() =>
                    client.close()))
        .then(table => res.redirect(table._id)));

router.get('/:tableID', (req, res, next) =>
    connectToDB()
        .then(({ client, tables }) =>
            tables
                .find({
                    _id: req.params.tableID
                })
                .limit(1)
                .next()
                .finally(() => client.close()))
        .then(table =>
            table ?
                res.render('annotateTable', prepareTable(table))
                :
                next(createError(404, `Table with id ${req.params.tableID} does not exists`)))
);

router.post('/:tableID', (req, res) => {
    const header = req.body.headerAnnotations;
    const data = req.body.dataAnnotations;
    if (!header || !data) {
        res.send(422);
    } else {
        connectToDB()
            .then(({client, tables}) =>
                tables
                    .update(
                        {
                            _id: req.params.tableID
                        },
                        {
                            $set:
                                {
                                    annotation: {
                                        header: req.body.headerAnnotations,
                                        data: req.body.dataAnnotations
                                    },
                                }
                        }
                    )
                    .finally(() => client.close())
            ).then(() => res.send(200))
    }
});

router.post('/:tableID/skip', (req, res) =>
    connectToDB()
        .then(({client, tables}) =>
            tables
                .update(
                    {
                        _id: req.params.tableID
                    },
                    {
                        $set:
                            {
                                skipped: true
                            }
                    }
                )
                .finally(() => client.close())
        ).then(() => res.send(200))
);

const prepareTable = table => {
    const headerRows = table.tableHeaders;
    const dataRows = table.tableData;
    normalizeColRowSpans(headerRows);
    normalizeColRowSpans(dataRows);
    const labelControls = [
        {
            label: 'Header',
            color: 'light-blue'
        }, {
            label: 'Data',
            color: 'lime'
        }, {
            label: 'Other',
            color: 'orange'
        }
    ];
    const headerAnnotations = new Array(headerRows.length).fill('Header');
    const dataAnnotations = new Array(dataRows.length).fill('Data');

    return {
        title: table.pgTitle,
        tableSource: `https://en.wikipedia.org/?curid=${table.pgId}`,
        headerRows,
        dataRows,
        labelControls,
        headerAnnotations,
        dataAnnotations,
        initialState: {
            headerAnnotations,
            dataAnnotations,
            id: table._id,
        }
    }
};

const normalizeColRowSpans = rows =>
    rows.forEach(row =>
        row.forEach(cell => {
            cell.tdHtmlString = cell.tdHtmlString.replace(/colspan=(["'])\d+(["'])/, 'colspan="1"');
            cell.tdHtmlString = cell.tdHtmlString.replace(/rowspan=(["'])\d+(["'])/, 'colspan="1"');
        })
    );

export default router;
