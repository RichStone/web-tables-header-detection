import express from 'express';
import createError from 'http-errors';
import { ObjectID } from "mongodb";
import { connectToDB } from '../helpers/mongo';
import config from "config";

const router = express.Router();

router.get('/:pageID', (req, res, next) =>
    connectToDB()
        .then(({ client, db }) => {
            db.collection(config.get('mongodb.collections.pages'))
                .find({
                    _id: ObjectID(req.params.pageID)
                })
                .limit(1)
                .next()
                .then(page => Promise.resolve(page.HTML))
            .finally(() => client.close())
        })
        .then(html =>
            source ?
                res.render('source', { html })
                :
                next(createError(404, `Page with id ${req.params.pageID} does not exist`)))
);

export default router;