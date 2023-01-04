for k=1:length(Pupil_data) 
    row = Pupil_data(k);
    if row.Group == "off-ADHD"
        writetable(row.Task_data, ['subject_' num2str(row.Subject) '_off_ADHD.csv']);
    elseif row.Group == "Ctrl"
        writetable(row.Task_data, ['subject_' num2str(row.Subject) '_Ctrl.csv']);
    else
        writetable(row.Task_data, ['subject_' num2str(row.Subject) '_on_ADHD.csv']);
    end
end