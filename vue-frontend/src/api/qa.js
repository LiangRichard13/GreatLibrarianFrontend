import service from "@/utils/request";

export function getQAByExpirenceId(expId,uid) {
    return service({
        url: '/QA',
        method: 'get',
        params: {
            tpid: expId,
            uid:uid
        }
    })
}

export function distributeToOthers(data) {
    return service({
        url: '/QA',
        method: 'put',
        data:data
    })
}

export function rateQA(QAid,score) {
    return service({
        url: '/testProjectUser',
        method: 'delete',
        params:{
            QAid:QAid,
            score:score
        }
    })
}