import express from 'express';
import createError from 'http-errors';
import { ObjectId } from "mongodb";
import { connectToDB } from '../helpers/mongo';
import { prepareTable } from "../helpers/tableUtil";

const router = express.Router();

router.get('/next', (req, res) =>
    connectToDB()
        .then(({ client, tables }) =>
            tables
                .find({
                    annotatedAt : {
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
                    _id: ObjectId(req.params.tableID)
                })
                .limit(1)
                .next()
                .finally(() => client.close()))
        .then(table =>
            table ?
                res.render('annotateTable', prepareTable(table))
                :
                next(createError(404, `Table with id ${req.params.tableID} does not exist`)))
);

router.post('/:tableID', (req, res) => {
    const annotations = req.body.annotations;
    if (!annotations) {
        res.send(422);
    } else {
        connectToDB()
            .then(({client, tables}) =>
                tables
                    .update(
                        {
                            _id: ObjectId(req.params.tableID)
                        },
                        {
                            $set:
                                {
                                    annotations,
                                    annotatedAt: new Date().getTime()
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
                        _id: ObjectId(req.params.tableID)
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

export default router;
