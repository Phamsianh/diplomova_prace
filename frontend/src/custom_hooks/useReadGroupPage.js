import {useEffect, useState} from 'react'
import { useController } from '../controllers';
import { displayGroups } from '../utils/cy';

export const useReadGroupPage = () => {
    const [groups_data, setGroupsData] = useState();
    const [cy, setCy] = useState();
	const { GroupCtlr } = useController();

	useEffect(() => {
		GroupCtlr.get_rsc_col().then((data) => {
			// console.log('groups data', data);
			setGroupsData(data);
		});
	}, []);

  useEffect(() => {
    if(!groups_data) return
    setCy(displayGroups("groups-cy", groups_data))
  }, [groups_data])

  return {
      groups_data,
      setGroupsData,
      cy,
      setCy
  }
}
