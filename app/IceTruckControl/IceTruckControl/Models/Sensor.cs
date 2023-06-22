using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IceTruckControl.Models
{

    // TODO: Decide on which way the model should work and if a DataHandler is needed
    public class Sensor
    {
        public int SensorId { get; private set; }
        public String SensorName { get; private set; }
        public float CurrentTempMeasured { get; set; }
        // TODO: Do some Unix Timestamp Magic in set method
        public DateTime TimeRecorded { get; set; }
    }
}
