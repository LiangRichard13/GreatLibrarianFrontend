import service from "@/utils/request";

export function getExperimentByProjectId(id) {
    return service({
        url: '/project/getExperimentByProjectId',
        method: 'get',
        params:{
            id:id
        }
    })
}

export function deleteById(id) {
    return service({
        url: '/project/deleteById',
        method: 'delete',
        params:{
            id:id
        }
    })
}