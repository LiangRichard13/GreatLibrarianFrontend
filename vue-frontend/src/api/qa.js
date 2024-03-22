import service from "@/utils/request";

//查询某测试下的QA
export function getQAByExpirenceId(expId,uid) {
    return service({
        url: '/QA',
        method: 'get',
        params: {
            tpid: expId,
            uid:uid,
            choose:1
        }
    })
}

//查询某测试下的QA条数
export function getQACount(expId) {
    return service({
        url: '/QA',
        method: 'get',
        params: {
            tpid: expId,
            choose:2
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