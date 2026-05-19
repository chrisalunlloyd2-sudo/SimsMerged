module com.simsneo {
    requires javafx.controls;
    requires javafx.fxml;
    requires com.fasterxml.jackson.databind;

    opens com.simsneo to javafx.fxml;
    exports com.simsneo;
    exports com.simsneo.engine;
    exports com.simsneo.model;
}
