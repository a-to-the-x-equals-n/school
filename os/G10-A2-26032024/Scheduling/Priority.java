/**
 * Priority scheduling algorithm.
 */
 
import java.util.*;

public class Priority implements Algorithm
{
    private List<Task> queue;
    private Task currentTask;

    private int tasksRun;

    public Priority(List<Task> queue) {
        this.queue = queue;

        tasksRun = queue.size();
    }

    public void schedule() {
        System.out.println("Priority Scheduling \n");

        while (!queue.isEmpty()) {
            currentTask = pickNextTask();
            
            CPU.run(currentTask, currentTask.getBurst());

            // remove the task
            queue.remove(currentTask);
        }
    }

    public Task pickNextTask() {

        //Holds task with highest priority
        //Puts first task in queue in highPri
        Task highPri = (Task)this.queue.get(0);
        
        //Highest priority value
        int pri = highPri.getPriority();

        //Loop through task queue
        for(int i = 1; i < queue.size(); i++) {

            //Current task
            Task curr = (Task)this.queue.get(i);
            //Priority of current task
            int currPri = curr.getPriority();

            //If priority of current task is higher than highest priority encountered
            //change highest priority task to current task
            if(currPri > pri) {
                pri = currPri;
                highPri = curr;
            }
        }

        //Return the highest priority
        return highPri;
    }
}
