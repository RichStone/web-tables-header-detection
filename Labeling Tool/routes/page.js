import express from 'express';
import createError from 'http-errors';
import config from "config";
import { ObjectId } from "mongodb";
import { connectToDB } from '../helpers/mongo';

const router = express.Router();

router.get('/:pageID', (req, res, next) => {
    const find = config.get('pgIdIsNumber') ? { pgId: Number(req.params.pageID) } : { pgId: ObjectId(req.params.pageID) };
    return connectToDB()
        .then(({client, db}) =>
            db.collection(config.get('mongodb.collections.pages'))
                .find(find)
                .limit(1)
                .next()
                .catch(console.error)
                .finally(() => client.close())
        )
        .then(page =>
            page ?
                res.send(page.HTML.replace('collapsed', ''))
                :
                next(createError(404, `Page with id ${req.params.pageID} does not exist`)));
});

export default router;