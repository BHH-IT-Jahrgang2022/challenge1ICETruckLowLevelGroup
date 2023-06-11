using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IceTruckControl.Models
{
    public class Sensor
    {
        public int SensorId { get; private set; }
        public String SensorName { get; private set; }
        public float CurrentTempMeasured { get; set; }
        public DateTime TimeRecorded { get; set; }
        public Sensor(String SensorName)
        {
            this.SensorName = SensorName;
        }
        public void SetNewMeasurement(float TempMeasured)
        {
            TimeRecorded = DateTime.Now;
            CurrentTempMeasured = TempMeasured;
            Debug.WriteLine($"Measured {TempMeasured}°C at {TimeRecorded}");
        }

    }
}
