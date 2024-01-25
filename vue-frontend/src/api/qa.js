import service from "@/utils/request";

export function getQAByExpirenceId(expId,uid) {
    return service({
        url: '/project/getQAByExpirenceId',
        method: 'get',
        params: {
            TPid: expId,
            uid:uid
        }
    })
}

export function distributeToOthers(data) {
    return service({
        url: '/project/distributeToOthers',
        method: 'put',
        data:data
    })
}

export function rateQA(QAid,score) {
    return service({
        url: '/project/rateQA',
        method: 'delete',
        params:{
            QAid:QAid,
            score:score
        }
    })
}